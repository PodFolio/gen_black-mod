import blackwood

name= "H:\\github\\gen_black\\Input\\splr\\XR.vob"

s= blackwood.blk_file() 
s.load(name)
 

# me: sub objetos

for me in range(1, 240):   
    s.set_mid(me)   
    ti = s.dump_mesh_as_string2()
    open("H:\\github\\gen_black\\Dump\\XR_%i.obj"%(me),"w").write("".join(ti))
    print "MESH ", me, "DONE"

    
