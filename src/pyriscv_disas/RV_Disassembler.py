'''
Copyright (c) 2018, University of North Carolina at Charlotte. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Authors: Reza Baharani - Transformative Computer Systems Architecture Research (TeCSAR) at UNC Charlotte
'''

from .riscv_disas import *

decompress_inst = {
    rv32: decompress_inst_rv32,
    rv64: decompress_inst_rv64,
    rv128: decompress_inst_rv128
}

unconditional_branches = [rv_op_ret, rv_op_jr, rv_op_jal, rv_op_jalr, rv_op_ecall, rv_op_ebreak, rv_op_uret, 
                          rv_op_sret, rv_op_hret, rv_op_mret, rv_op_dret, rv_op_c_jal, rv_op_c_j,
                          rv_op_c_jr, rv_op_c_ebreak, rv_op_c_jalr, rv_op_j]

conditional_branches = [rv_op_beqz, rv_op_bnez, rv_op_bltz, rv_op_bgtz, rv_op_bgt, rv_op_blez, rv_op_bgez, rv_op_ble,
                        rv_op_bgtu, rv_op_bleu, rv_op_beq, rv_op_bne, rv_op_blt, rv_op_bge, rv_op_bltu, rv_op_bgeu,
                        rv_op_c_beqz, rv_op_c_bnez]

load_instructions = [rv_op_lui, rv_op_lb, rv_op_lh, rv_op_lw, rv_op_lbu, rv_op_lhu, rv_op_lwu, rv_op_ld, rv_op_ldu, rv_op_lq,
                     rv_op_lr_w, rv_op_lr_d, rv_op_lr_q, rv_op_flw, rv_op_fld, rv_op_flq, rv_op_c_fld, rv_op_c_lw, rv_op_c_flw, rv_op_c_li,
                     rv_op_c_lui, rv_op_c_fldsp, rv_op_c_lwsp, rv_op_c_flwsp, rv_op_c_ld, rv_op_c_ldsp, rv_op_c_lq, rv_op_c_lqsp]

store_instructions = [rv_op_sb, rv_op_sh, rv_op_sw, rv_op_sd, rv_op_sq, rv_op_sc_w, rv_op_sc_d, rv_op_sc_q, rv_op_fsw, rv_op_fsd,
                      rv_op_fsq, rv_op_c_fsd, rv_op_c_sw, rv_op_c_fsw, rv_op_c_fsdsp, rv_op_c_swsp, rv_op_c_fswsp, rv_op_c_sd, 
                      rv_op_c_sdsp, rv_op_c_sqsp, rv_op_c_sq]

synch_instruction = [rv_op_fence, rv_op_fence_i, rv_op_sfence_vm, rv_op_sfence_vma]





class Inst(rv_decode):
    '''
        I defined these four catagories for my own purpose:
            0. R(egister) -> Register type (Doing nothing with outside)
            1. M(emory)   -> Memories instructions (load and store)
            3. C(ontrol)  -> Branches (Conditional and Unconditional)
            4. S(ynch)    -> Fence instructions
    '''
    instruction_type = {
        -1: "Illigal",
        0: "R",
        1: "M",
        2: "C",
        3: "S"
    }

    def __init__(self):
        super().__init__()
        self.src_register = set()
        self.dest_register = set()
        self.analyzed = False
        self.type = -1

    def anlz_accesses(self):
        metadata = get_opcode_data(self.op)
        fmt = metadata.format

        if (self.op in unconditional_branches or self.op in conditional_branches):
            self.type = 2 # It is a control instruction
        elif (self.op in store_instructions or self.op in load_instructions):
            self.type = 1
        elif self.op in synch_instruction:
            self.op = 3
        elif self.op != 0:
            self.type = 0

        if fmt == rv_fmt_none: # 1
            pass
        if (fmt == rv_fmt_rd_imm or fmt==rv_fmt_rd_offset): # 2 3
            self.dest_register.add(self.rd)
        elif fmt == rv_fmt_rd_rs1_offset: # 4
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rs1_rs2_offset:# 5
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rd_offset_rs1: # 6
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rs2_offset_rs1: # 7
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rd_rs1_imm: # 8
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rd_rs1_rs2: # 9
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_aqrl_rd_rs1: # 10
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_aqrl_rd_rs2_rs1: # 11
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rd_csr_rs1: # 12
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rd_csr_zimm: # 13
            self.dest_register.add(self.rd)
        elif fmt == rv_fmt_frd_offset_rs1: # 14
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_frs2_offset_rs1: # 15
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rm_frd_frs1_frs2_frs3: # 16
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
            self.src_register.add(self.rs3)
        elif fmt == rv_fmt_frd_frs1_frs2: # 17
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rd_frs1_frs2: # 18
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rm_rd_frs1: # 19
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rm_frd_rs1: # 20
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_frd_rs1: # 21
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rs1: # 22
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_offset: # 23
            pass # Jump
        elif fmt == rv_fmt_pred_succ: # 24
            pass # fences
        elif fmt == rv_fmt_rs1_rs2: # 25
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rd_frs1: # 26
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rm_frd_frs1: # 27
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rm_frd_frs1_frs2: # 28
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rs2_rs1_offset: # 29
            self.src_register.add(self.rs1)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rd: # 30
            self.dest_register.add(self.rd)
        elif fmt == rv_fmt_rd_zimm: # 31
            self.dest_register.add(self.rd)
        elif fmt == rv_fmt_rd_rs1: # 32
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rd_rs2: # 33
            self.dest_register.add(self.rd)
            self.src_register.add(self.rs2)
        elif fmt == rv_fmt_rs1_offset: # 34
            self.src_register.add(self.rs1)
        elif fmt == rv_fmt_rs2_offset: # 35
            self.src_register.add(self.rs2)

    @property
    def write_access(self):
        if not self.analyzed:
            self.anlz_accesses()
        return self.dest_register
    
    @property
    def read_access(self):
        if not self.analyzed:
            self.anlz_accesses()
        return self.src_register
    
    @property
    def fmt_type(self):
        if not self.analyzed:
            self.anlz_accesses()
        return Inst.instruction_type[self.type]

    def format(self, str_buffer_size = 128, tab_size = 32):
        buf = bufArray(str_buffer_size)
        format_inst(buf, str_buffer_size, tab_size, self)
        fmt = '0x{:x}'.format(self.pc)+ ': 0x' + ''.join(buf[i].encode('utf-8', 'surrogateescape').decode('utf-8', 'replace') for i in range(str_buffer_size))
        return fmt

    def __repr__(self):
        return self.format
    
    def __str__(self):
        return self.format


class rv_disas:
    def __init__(self, PC, arch = rv64):
        self.arch = arch
        self.init_PC = PC
        self._PC = PC

    @property
    def PC(self):
        return self._PC

    def disassemble(self, inst):
            dec = Inst() #rv_decode()
            dec.pc = self._PC
            dec.inst = inst
            decode_inst_opcode(dec, self.arch)
            decode_inst_operands(dec)
            decompress_inst[self.arch](dec)
            decode_inst_lift_pseudo(dec)
            self._PC += inst_length(inst) 
            return dec



if __name__ == "__main__":

    '''
        81686:	1101                	addi	sp,sp,-32
        81688:	e426                	sd	s1,8(sp)
        8168a:	e822                	sd	s0,16(sp)
        8168c:	d581b403          	ld	s0,-680(gp) # b0070 <global>
        81690:	ec06                	sd	ra,24(sp)
        81692:	c805                	beqz	s0,816c2 <freeres+0x3c>
        81694:	7008                	ld	a0,32(s0)
        81696:	c519                	beqz	a0,816a4 <freeres+0x1e>
        81698:	892de0ef          	jal	ra,5f72a <conf_decrement>
        8169c:	d581b403          	ld	s0,-680(gp) # b0070 <global>
        816a0:	02043023          	sd	zero,32(s0)
        816a4:	6808                	ld	a0,16(s0)
        816a6:	ef9d80ef          	jal	ra,5a59e <__free>
        816aa:	d581b503          	ld	a0,-680(gp) # b0070 <global>
        816ae:	00043423          	sd	zero,8(s0)
        816b2:	00043023          	sd	zero,0(s0)
        816b6:	00043823          	sd	zero,16(s0)
        816ba:	ee5d80ef          	jal	ra,5a59e <__free>
        816be:	d401bc23          	sd	zero,-680(gp) # b0070 <global>
        816c2:	60e2                	ld	ra,24(sp)
        816c4:	6442                	ld	s0,16(sp)
        816c6:	64a2                	ld	s1,8(sp)
        816c8:	6105                	addi	sp,sp,32
        816ca:	8082                	ret
   '''
    inst_arr = [0x1101, 0xe426, 0xe822, 0xd581b403, 0xec06, 0xc805, 0x7008, 0xc519, 0x892de0ef, 0xd581b403, 0x02043023, 0x6808, 0xef9d80ef, 
                0xd581b503, 0x00043423, 0x00043023, 0x00043823, 0xee5d80ef, 0xd401bc23, 0x60e2, 0x6442, 0x64a2, 0x6105, 0x8082]
    machine = rv_disas(PC=0x81686)

    for ins in inst_arr:
        decd_inst = machine.disassemble(ins)
        print(decd_inst.format())
        print('\t Read Registers  : ' + str(decd_inst.read_access))
        print('\t Write Registers : ' + str(decd_inst.write_access))
        print('\t Instruction type: ' + decd_inst.fmt_type)
        print('------------------------')
