import riscv_disas

decompress_inst = {
    riscv_disas.rv32: riscv_disas.decompress_inst_rv32,
    riscv_disas.rv64: riscv_disas.decompress_inst_rv64,
    riscv_disas.rv128: riscv_disas.decompress_inst_rv128
}

class Inst(riscv_disas.rv_decode):
    def read_access(self):
        return set([self.rs1, self.rs2, self.rs3])
    
    def write_access(self):
        return self.rd

    def format(self, str_buffer_size = 128, tab_size = 32):
        buf = riscv_disas.bufArray(str_buffer_size)
        riscv_disas.format_inst(buf, str_buffer_size, tab_size, self)
        fmt = ''.join(buf[i].encode('utf-8', 'surrogateescape').decode('utf-8', 'replace') for i in range(str_buffer_size))
        return fmt




class rv_disas:
    def __init__(self, PC, arch = riscv_disas.rv64):
        self.arch = arch
        self.init_PC = PC
        self._PC = PC

    @property
    def PC(self):
        return self._PC

    def disassemble(self, inst):
            dec = Inst() #riscv_disas.rv_decode()
            dec.pc = self._PC
            dec.inst = inst
            riscv_disas.decode_inst_opcode(dec, self.arch)
            riscv_disas.decode_inst_operands(dec)
            decompress_inst[self.arch](dec)
            riscv_disas.decode_inst_lift_pseudo(dec)
            self._PC += riscv_disas.inst_length(inst) 
            return dec



if __name__ == "__main__":

    inst_arr = [0x0, 0x1, 0xd, 0x401, 0x404, 0x405, 0xf1402573, 0x597, 0x204002b7, 0x13]
    machine = rv_disas(PC=0x10078)

    for ins in inst_arr:
        decd_inst = machine.disassemble(ins)
        print(decd_inst.format())
        print('\t Read Registers:' + str(decd_inst.read_access()))
        print('\t Write Registers:' + str(decd_inst.write_access()))
        print('------------------------')

    '''
    inst_arr = [0x0, 0x1, 0xd, 0x401, 0x404, 0x405, 0xf1402573, 0x597, 0x204002b7, 0x13]
    buf = bufArray(128)
    dec = rv_decode()
    dec.pc = 0x10078
    dec.inst = inst_arr[0]
    decode_inst_opcode(dec, rv64)
    decode_inst_operands(dec)
    decompress_inst_rv64(dec)
    decode_inst_lift_pseudo(dec)
    format_inst(buf, 128, 32, dec)
    for i in range(128):
        print(buf[i].encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'), end='')
    print()

    def print_insn(pc, inst):
    	buf = bufArray(128)
    	disasm_inst(buf, 128, rv64, pc, inst)
    	for i in range(128):
    		print(buf[i].encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'), end='')
    	print()

    if __name__ == "__main__":
    	pc = 0x10078
    	for inst in inst_arr:
    		print_insn(pc, inst)
    		pc += inst_length(inst)
    '''