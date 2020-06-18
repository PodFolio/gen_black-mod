import blackwood


name= "D:\\Games\\LFS\\data\\veh\\modding\\lfsdk\\Export\\rims.cem"
#name= "D:\\Documents and Settings\User\\Desktop\\LFS_S2_ALPHA_Z\\data\\wld\\Blackwood.wld"
#name= "C:\\Documents and Settings\\Henrique.CATALDO-FE60ADE\\Desktop\\Conversor\\FX.vob"

#name= "D:\\Documents and Settings\\Henrique.CATALDO-FE60ADE\\Desktop\\Conversor\\ALTEZZA.vob"

 

s= blackwood.blk_file() 
s.load(name)
 

# me: sub objetos

for me in range(1, 80):   
    s.set_mid(me)   
    ti = s.dump_mesh_as_string()
    open("dump\\ALTEZZA_%i.obj"%(me),"w").write("".join(ti))
    print "MESH ", me, "DONE"

    
