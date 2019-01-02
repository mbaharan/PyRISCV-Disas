%module riscv_disas
%{
	/* Includes the header in the wrapper code */
	#include "riscv-disas.h"
	#include "riscv-disas.c"
%}

/* Parse the header file to generate wrappers */
%include "riscv-disas.h"
%include "riscv-disas.c"
%include stdint.i
%include carrays.i
%array_class(char, bufArray);






