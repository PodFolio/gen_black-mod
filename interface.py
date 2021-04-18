#interface

import compiler
compiler.compileFile("H:\\github\\gen_black\\blackwood.py")
compiler.compileFile("H:\\github\\gen_black\\gen_black.py")

base_dir="H:\\github\\gen_black\\Input\\splr\\"

file_command="cmd6.txt"


file_input="H:\\github\\gen_black\\Base\\R\\XR.vob"



import os
import gen_black

os.chdir( base_dir)
gen_black.process( file_command, file_input )

print "DONE"
