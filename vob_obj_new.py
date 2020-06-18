import blackwood

name= "C:\\Blackwood.wld"

s= blackwood.blk_file() 
s.load(name)
 

# me: sub objetos

for me in range(1, 110):   
    s.set_mid(me)   
    ti = s.dump_mesh_as_string()
    open("C:\\dump\\Blackwood_%i.obj"%(me),"w").write("".join(ti))
    print "MESH ", me, "DONE"

    
