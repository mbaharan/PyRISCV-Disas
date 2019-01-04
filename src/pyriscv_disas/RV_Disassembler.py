from .riscv_disas import *

decompress_inst = {
    rv32: decompress_inst_rv32,
    rv64: decompress_inst_rv64,
    rv128: decompress_inst_rv128
}

class Inst(rv_decode):
    def __init__(self):
        super().__init__()
        self.src_register = set()
        self.dest_register = set()
        self.analyzed = False

    def anlz_accesses(self):
        fmt = get_opcode_data(self.op).format

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
        print('\t Read Registers:' + str(decd_inst.read_access))
        print('\t Write Registers:' + str(decd_inst.write_access))
        print('------------------------')
