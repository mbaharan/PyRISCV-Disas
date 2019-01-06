'''
Copyright (c) 2018, University of North Carolina at Charlotte. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Authors: Reza Baharani - Transformative Computer Systems Architecture Research (TeCSAR) at UNC Charlotte
'''

from pyriscv_disas import Inst, rv_disas

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
