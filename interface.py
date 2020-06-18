#interface

import compiler
compiler.compileFile("F:\\LFS\\gen_black\\dist\\blackwood.py")
compiler.compileFile("F:\\LFS\\gen_black\\dist\\gen_black.py")

base_dir="F:\\LFS\\gen_black\\dist\\Input\\mx5rim\\"

file_command="rims.txt"

#file_input="F:\\LFS\\gen_black\\dist\\Input\\xr_base\\XR_base.vob"
file_input="F:\\LFS\\gen_black\\dist\\Input\\mx5rim\\base_rim_mod.vob"



import os
import gen_black

os.chdir( base_dir)
gen_black.process( file_command, file_input )

print "DONE"
