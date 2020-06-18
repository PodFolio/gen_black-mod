#interface

import compiler
compiler.compileFile("blackwood.py")
compiler.compileFile("gen_black.py")



file_command="cmd.txt"


file_input="C:\\Users\\damian\\Downloads\\RevBouncer\\lfsdk\\lfsdk\\Inport\\XF.vob"



import os
import gen_black

os.chdir( base_dir)
gen_black.process( file_command, file_input )

print "DONE"
