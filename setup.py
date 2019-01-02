import sys
import os
from setuptools import setup, find_packages, Extension

libPath = "./c_core"

module_lib_riscv_disas = Extension(
      name = '_riscv_disas', 
      sources = [
            os.path.join(libPath, 'riscv-disas_wrap.c')
      ]
)
setup (
      name = 'riscv_disas',
      version = '0.1',
      author = "Reza Baharani",
      description = "Python binding for RISC-V Disassembler",
      packages= find_packages(where = 'src/riscv-disas'),
      package_dir = {'':'src/riscv-disas'},
      ext_modules=[module_lib_riscv_disas]
)
