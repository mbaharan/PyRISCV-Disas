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
      name = 'PyRiscv_disas',
      version = '0.2',
      author = "Reza Baharani",
      author_email="mbaharan (at) uncc.edu",
      license="MIT",
      description = "Python binding for RISC-V disassembler",
      packages= ['pyriscv_disas'],
      package_dir = {'':'./src/'},
      ext_modules=[module_lib_riscv_disas]
)
