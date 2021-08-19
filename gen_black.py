#base_dir="C:\\LFSDK\\CARS"
#file_command="cars.txt"
#file_input="C:\\LFSDK\\Inport\\xr.vob"

import blackwood
import objread


def get_optimized_vertex(  vlist , tol=0.001):
    #3ds eh tolo em otimizar os vertices
    n= len(vlist)
    vl=[ i+0 for i in range(n) ]
    return vl

    gs=0
    for i in range(n-1):
      for j in range(i+1,n):
        if abs(vlist[i][0]-  vlist[j][0])< tol  and abs(vlist[i][1]-  vlist[j][1])< tol and abs(vlist[i][2]-  vlist[j][2])< tol:
            vl[j]=i+0
            gs+=1
    msg(" vertex reconect %i"%(gs))        
    return vl            
        

def msg(s):
    print s
 
def process( file_command, file_input  ):
  lns= open( file_command , "r" )

  o_vt, obj , obj_uv = {},{},{}
  vtab={}  #buffer for vertex
  for i in range(len(o_vt)): vtab[i]=None
  
  #set vars
  vob= blackwood.blk_file()
  vob.load(file_input  )  
  mirror = 1  #on
  imodel=0  #actual model
  vop=[]
  print "OBJ NAMES"
  for k in vob.get_obj_names():
      print k, " "*(20-len(k) ) ,  vob.get_obj_file_texture(k)
   
  enable = True
  for l in lns:
    li =l.split()
    if len(li)==0: continue
    if li[0]=="#": continue
    cmd= li[0].upper()
    print "___"*6
    print ">", l

    if cmd == "ENABLE":
       enable == True
    if cmd == "DISABLE":
       enable == False
       

    if enable == False:
       continue 

    
    if cmd=="LOAD":
         file_obj=li[1]
         o_vt, obj , obj_uv =objread.read_obj_faces_names( file_obj )
         vtab={}  #buffer for vertex
         for i in range(len(o_vt)): vtab[i]=None 
         vop= get_optimized_vertex( o_vt ) 
        
    if cmd=="MIRROR":
       if li[1].upper() == "ON":
          msg("MIRROR ON")  
          mirror=1 
       if li[1].upper() == "OFF":
          msg("MIRROR OFF")             
          mirror=0            
       if li[1].upper() == "FIX":
          msg("MIRROR FIX")             
          mirror=2
       if li[1].upper() == "GLASS":
          msg("MIRROR GLASS")             
          mirror=3
       if li[1].upper() == "FIX2":
          msg("MIRROR FIX2")             
          mirror=4
       if li[1].upper() == "FIX3":
          msg("MIRROR FIX3")             
          mirror=5	
       if li[1].upper() == "BODYOFF":
          msg("MIRROR BODY OFF")             
          mirror=6
       if li[1].upper() == "BODYON":
          msg("MIRROR BODY ON")             
          mirror=7
       if li[1].upper() == "BODYFIX":
          msg("MIRROR BODY FIX")             
          mirror=8		  

    if cmd=="POSITION":
       if li[1].upper() == "M":
          msg("MIRROR ON")  
          mirror=1 
       if li[1].upper() == "I":
          msg("DRIVER POSITION")             
          mirror=0            
       if li[1].upper() == "0":
          msg("POSITION 0")             
          mirror=2
		  
    if cmd=="GLUE": 
       obj_name=li[1]
       obj2_name=li[2]
       dist=float(li[3])
       print "clean model",obj_name,obj2_name
       o_fc1= obj[ obj_name] 
       o_fc2= obj[ obj2_name]
       obj[ obj_name] = vob.glue_vertex( o_vt , o_fc1, o_fc2 , dist  )

    if cmd=="MESH":
       mid=int(li[1])
       msg("set mesh as %i"%(mid))
       vob.set_mid(mid)
       vtab={}
       for i in range(len(o_vt)): vtab[i]=None 
       print "OBJ NAMES"
       for k in vob.get_obj_names():
         print k


    if cmd=="SUBMESHES_COUNT":
       sub = int(li[1])
       msg("sub mesh count %i" % (sub))
       vob.set_mid(1)
       vob.set_child(sub)

    if cmd=="MIRROR_STATE":
       m_s = li[1]
       if m_s.upper() == "MIRROR_ONLY":
          msg("MIRROR ONLY")
          mirror_s=227
       if m_s.upper() == "MIRROR_FIX_POSSIBLE":
          msg("MIRROR FIX POSSIBLE")
          mirror_s=226
       vob.set_mirror_state(mirror_s)

    if cmd=="MESH_TYPE":
        m_t = li[1]
        if m_t.upper() == "MAIN":
           msg("MAIN MESH")
           mesh_t=0
        if m_t.upper() == "CALIPER":
           msg("BRAKE CALIPER")
           mesh_t=1
        if m_t.upper() == "WHEEL":
           msg("STEERING WHEEL")
           mesh_t=2
        if m_t.upper() == "DEFAULT":
           msg("DEFAULT MESH")
           mesh_t=3
        if m_t.upper() == "ALWAYS_VISIBLE":
           msg("ALWAYS VISIBLE, EVEN IN F MODE")
           mesh_t=5
        if m_t.upper() == "MIRROR":
           msg("CENTRAL REARVIEW MIRROR")
           mesh_t=10
        vob.set_mesh_type(mesh_t)

    if cmd=="MESH_FIX":
       m_f = li[1]
       if m_f.upper() == "ON":
          msg("MIRROR FIX WORKS")
          mesh_f=1
       if m_f.upper() == "OFF":
          msg("MIRROR FIX NOT WORK")
          mesh_f=2
       vob.set_mesh_fix(mesh_f)

    if cmd == "EXIT":
        break 
        
    if cmd=="DELETE_ALL" or cmd=="CLEAN_ALL" :
       #vob_name=li[0]
       df=0
       g= vob.get_obj_names()  
       dd=[  0 for i in range(vob.nf) ]
 
       for ij in range(vob.mn) : 
          flist= vob.get_face_list_id( ij )
          flist.sort()           
          msg("Delete %s"%(g[ij]) )
          for j in range( vob.nf -1, -1,-1): 
            fii= vob.off_fc + j*12  
            if (vob.data[fii+2] != ij ) or (vob.data[fii+4] !=0 ):
                #if vob.face_is_safe( j ):
                   vob.delete_face( j )
 
           


    if cmd=="MODEL":
       imodel= int(li[1])
       
    # if cmd=="DELETE_MODEL" or cmd=="CLEAN_MODEL" :        
       # vob_name=li[1] 
       # df=0
       # g= vob.get_obj_names()  
       # if not(vob_name in g):
          # msg("PART %s NOT FOUND "%(vob_name) ) 
       # else:
          # flist= vob.get_face_list(vob_name ,models=[ imodel ]  )
          # flist.sort()           
          # msg("Delete %s"%(vob_name) )
          # for i in range(len(flist)-1, -1,-1):
              # vob.delete_face_model( flist[i],imodel )
              # df+=1
          # msg("%i faces deleted "%(df) )


 
    if cmd=="DELETE_COL" or cmd=="CLEAN_COL" :
        
       vob_name=li[1]
       g= vob.get_obj_names()  
       if not(vob_name in g):
          msg("PART %s NOT FOUND "%(vob_name) ) 
       else:
          vob.delete_faces_col( vob_name  )


    if cmd=="DELETE_SHADOW" or cmd=="CLEAN_SHADOW" :
        
       vob_name=li[1]
       g= vob.get_obj_names()  
       if not(vob_name in g):
          msg("PART %s NOT FOUND "%(vob_name) ) 
       else:
          vob.delete_faces_shadow( vob_name  )

    if cmd=="DELETE_MODEL" or cmd=="CLEAN_MODEL" or cmd=="DEL_M" :
        
       vob_name=li[1]
       #imodel= int(li[2])
       g= vob.get_obj_names()  
       if not(vob_name in g):
          msg("PART %s NOT FOUND "%(vob_name) ) 
       else:
          vob.delete_faces_model( vob_name, model=imodel  )

    if cmd=="DEL" :
        
       vob_name=li[1]
       shadow= int(li[2])
       nomodel= int(li[3])
       g= vob.get_obj_names()  
       if not(vob_name in g):
          msg("PART %s NOT FOUND "%(vob_name) ) 
       else:
          if nomodel==-1:
			vob.delete_faces_norm( vob_name, shadow )
          else:
            vob.delete_faces_del( vob_name, shadow, nomodel )
          
          
    if cmd=="DELETE" or cmd=="CLEAN" :
        
       vob_name=li[1]
       df=0
       g= vob.get_obj_names()  
       if not(vob_name in g):
          msg("PART %s NOT FOUND "%(vob_name) ) 
       else:
          flist= vob.get_face_list(vob_name  )
          flist.sort()
          print "will delete ",len(flist)
          msg("Delete %s"%(vob_name) )
          for i in range(len(flist)-1, -1,-1):
              vob.delete_face( flist[i] )
              df+=1
          msg("%i faces deleted "%(df) )    

    if cmd=="ADD": 
       vob_name=li[1]
       obj_name=li[2]
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError 
       o_fc= obj[ obj_name  ]
       oid= gl.index( vob_name )
       recl=0
       fnew=0
       msg("ADD in %s  the contents of %s"%(vob_name, obj_name  ))
       vob.scan_vertex()
        
       #print "MIRROR = ", mirror
       for fi in range(len(o_fc)):
           ffj = vob.add_face()            
           vls=[]           #find 3 empty vertex
       
           for vk in [  o_fc[fi][0] ,o_fc[fi][1] ,o_fc[fi][2] ] :
               vo = vop[vk] +0
               
               if vtab[vo]==None   :
                  for vi in range(vob.nv)  :
                      if vob.vfree[vi]==0:
                         vob.vfree[vi]+=1 
                         vtab[vo] = vi+0
                         recl+=1
                         break                        
               if vtab[vo]==None :
                  vvk = vob.add_vertex()
                  vob.vfree[vvk]=1
                  fnew+=1                   
                  vtab[vo]=vvk+0          
                  
               vob.set_vertex( vtab[vo ], o_vt[vo][0],o_vt[vo][1],o_vt[vo][2] )
               #print vob.get_vertex( vtab[vo] ), o_vt[vo]
               vls.append(  vtab[vo] )               
           #print  vls
              
           vob.set_face( ffj, vls[0],vls[1],vls[2], oid ,mirror , model=imodel   )
           
 
       vob.scan_normals( oid  )        
       msg("reclicled %i vertex, new %i vertex"%(recl,fnew ))



    if cmd=="ADD_LOD1" or cmd=="ADD_SHADOW": 
       vob_name=li[1]
       obj_name=li[2]
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError 
       o_fc= obj[ obj_name  ]
       oid= gl.index( vob_name )
       recl=0
       fnew=0
       msg("ADD in %s  the contents of %s"%(vob_name, obj_name  ))
       vob.scan_vertex()
        
       #print "MIRROR = ", mirror
       for fi in range(len(o_fc)):
           ffj = vob.add_face()            
           vls=[]           #find 3 empty vertex
       
           for vk in [  o_fc[fi][0] ,o_fc[fi][1] ,o_fc[fi][2] ] :
               vo = vop[vk] +0
               
               if vtab[vo]==None   :
                  for vi in range(vob.nv)  :
                      if vob.vfree[vi]==0:
                         vob.vfree[vi]+=1 
                         vtab[vo] = vi+0
                         recl+=1
                         break                        
               if vtab[vo]==None :
                  vvk = vob.add_vertex()
                  vob.vfree[vvk]=1
                  fnew+=1                   
                  vtab[vo]=vvk+0          
                  
               vob.set_vertex( vtab[vo ], o_vt[vo][0],o_vt[vo][1],o_vt[vo][2] )
               #print vob.get_vertex( vtab[vo] ), o_vt[vo]
               vls.append(  vtab[vo] )               
           #print  vls
              
           vob.set_face( ffj, vls[0],vls[1],vls[2], oid ,mirror , model=imodel , aid =1  )
           
 
       vob.scan_normals( oid  )        
       msg("reclicled %i vertex, new %i vertex"%(recl,fnew ))

    if cmd=="ADD_LOD2" or cmd=="ADD_COL": 
       vob_name=li[1]
       obj_name=li[2]
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError 
       o_fc= obj[ obj_name  ]
       oid= gl.index( vob_name )
       recl=0
       fnew=0
       msg("ADD in %s  the contents of %s"%(vob_name, obj_name  ))
       vob.scan_vertex()
        
       #print "MIRROR = ", mirror
       for fi in range(len(o_fc)):
           ffj = vob.add_face()            
           vls=[]           #find 3 empty vertex
       
           for vk in [  o_fc[fi][0] ,o_fc[fi][1] ,o_fc[fi][2] ] :
               vo = vop[vk] +0
               
               if vtab[vo]==None   :
                  for vi in range(vob.nv)  :
                      if vob.vfree[vi]==0:
                         vob.vfree[vi]+=1 
                         vtab[vo] = vi+0
                         recl+=1
                         break                        
               if vtab[vo]==None :
                  vvk = vob.add_vertex()
                  vob.vfree[vvk]=1
                  fnew+=1                   
                  vtab[vo]=vvk+0          
                  
               vob.set_vertex( vtab[vo ], o_vt[vo][0],o_vt[vo][1],o_vt[vo][2] )
               #print vob.get_vertex( vtab[vo] ), o_vt[vo]
               vls.append(  vtab[vo] )               
           #print  vls
              
           vob.set_face( ffj, vls[0],vls[1],vls[2], oid ,mirror , model=imodel , aid =2 )
           
 
       vob.scan_normals( oid  )        
       msg("reclicled %i vertex, new %i vertex"%(recl,fnew ))


    if cmd=="ADJUST_TEXTURE_SIZE":
       vob_name= li[1]      
       
     
       rt = float(li[2])
       
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError
        
 
            
       morr = vob.get_orient_obj( vob_name )
       
       txid = vob.get_obj_texid(  vob_name )
       du,dv= vob.get_texture_slot_size(txid)

       print du,dv
       mat_name=  vob.get_obj_material(  vob_name  )  
       x1,x2, y1,y2= vob.get_material_bb(mat_name)
 
       print "limits originais",x1,x2,y1,y2 
       
       if x1*x2 > 0:
            extend==False
       else:
            extend=True
       pori= vob.get_orient_obj( vob_name )
       x1,x2,y1,y2 = vob.get_axis_limits( vob_name ,[0,1,2,3,4,5,6,7,8,9] ,pori )
       
       print "novos limites",x1,x2,y1,y2
       
       if extend and  morr != 3 :
          x2 = max( abs(x1),abs(x2) )
          x1 = -x2

       dx = abs(x2 -x1)
       dy = abs(y2 -y1)
       
       brt = du /float( dv )
       
       rt = rt* brt
       
       dyi = dy+0
       dxi = dx+0 
       


       
       
       while  dxi/dyi > rt :
           dyi = dyi*1.05
           
       while  dxi/dyi < rt :
           dxi = dxi*1.05
           


           
      
       sx= 1.0
       sy=1.0
       if dx>0 or dy >0 :
        sx = dxi /dx
        sy = dyi/ dy

       xm = 0.5*(x1+x2)
       ym = 0.5*(y1+y2)

       if extend: 
          px1,px2,py1,py2 = xm- dxi/2.0 , xm+dxi/2.0 , ym- dyi/2.0 , ym+dyi/2.0
       else:
          x1,x2, y1,y2= vob.get_material_bb(mat_name) 
          px1= x1
          px2= x1+dxi          
          py1= y1  
          py2= y1 + dyi
          
          
       
       mat_name=  vob.get_obj_material(  vob_name  )  
       x1,x2, y1,y2= vob.get_material_bb(mat_name)
       
       print x1,x2, y1,y2 , " ->  ", px1,px2,py1,py2
     
       vob.set_material_bb(  mat_name, px1,px2,py1,py2  )


    if cmd=="CHECK_BB":
       vob_name= li[1]  	
       mat_name=  vob.get_obj_material(  vob_name  )  
       x1,x2, y1,y2= vob.get_material_bb(mat_name)
       
       print x1,x2, y1,y2
	   
    if cmd=="SET_BB":
       vob_name= li[1] 
       px1 = float(li[2])
       px2 = float(li[3])	
       py1 = float(li[4])	
       py2 = float(li[5])		   
       mat_name=  vob.get_obj_material(  vob_name  )  
       print x1,x2, y1,y2 , " ->  ", px1,px2,py1,py2
       vob.set_material_bb(  mat_name, px1,px2,py1,py2  )
	   
    if cmd=="SCALE":
       vob_name= li[1] 
       scale = float(li[2])		   
       mat_name=  vob.get_obj_material(  vob_name  )  
       x1,x2, y1,y2= vob.get_material_bb(mat_name)
       px1 = x1 / scale
       px2 = x2 / scale
       py1 = y1 / scale
       py2 = y2 / scale
       print x1,x2, y1,y2 , " ->  ", px1,px2,py1,py2
       vob.set_material_bb(  mat_name, px1,px2,py1,py2  )
	   
    if cmd=="MOVE":
       vob_name= li[1] 
       side = float(li[2])
       updown = float(li[3])		   
       mat_name=  vob.get_obj_material(  vob_name  )  
       x1,x2, y1,y2= vob.get_material_bb(mat_name)
       if side < 0:
          px1 = x1 + side
          px2 = x2 + side
       else:
          px1 = x1 - side
          px2 = x2 - side          
       if updown < 0:
          py1 = y1 + updown
          py2 = y2 + updown
       else:
          py1 = y1 - updown
          py2 = y2 - updown
       print x1,x2, y1,y2 , " ->  ", px1,px2,py1,py2
       vob.set_material_bb(  mat_name, px1,px2,py1,py2  )      
        
    if cmd=="RENDER_TEMPLATE":
       vob_name= li[1]      
       file_temp= li[2]
       s_models= li[3:]       
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError  
       oid= gl.index( vob_name )
       for im in s_models:
          vob.render_template( oid, int(im) , file_temp)
          vob.render_template( oid, int(im) , file_temp,kside=1)  


         
    if cmd=="SET_TEXTURE_SLOT1":
       vob_name= li[1]
       dds_name= li[2]
       orient=   li[4].upper()
       extend=   li[3].upper()
       sp1=0
       if extend == "SINGLE":
           extend=False
       else:
            extend=True       
       slots = [ int(j) for j in li[5:] ]
       #print li
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError
       oid= gl.index( vob_name )
       dc= {"LSIDE":4,"SIDE":3,"TOP":5,"BACK":2,"FRONT":1}
       if not(orient in dc.keys()):
          msg("SET_TEXTURE_SLOT accep only side,top,back,front planes")
          msg("SIDE receive: %s"%(orient ))
       x1,x2,y1,y2 = vob.get_axis_limits( vob_name ,[0,1,2,3,4,5,6,7,8,9] ,dc[orient.upper()] )
       #print "->",x1,x2,y1,y2 
       if extend and dc[orient.upper()] != 3:
          x2 = max( abs(x1),(x2) )
          x1 = -x2          
       mti, nada,nada2 = vob.get_mat_info()
       mat_name =  vob_name +"@"
       if not(mat_name in nada2):
          vob.add_material(   mat_name)       
 
       vob.set_obj_material(oid,mat_name)
       #print "AFTER ->",x1,x2,y1,y2 
       if dc[orient.upper()] == 1 and extend == False:
          px1=x2
          px2=x1
       else:
          px1=x1
          px2=x2 
       vob.set_material_bb(  mat_name, x1,x2,y1,y2)
       tid = vob.get_obj_texid( vob_name )              
       tf,ti,mt= vob.get_mat_pos()
       vi = ti[0] + tid * 24
       shin= vob.data[vi+16 ]+0

        
       tex_mirror= True 
       if dc == 3 : tex_mirror=False
       u,v,du,dv = blackwood.calc_slot( [ int( ki) for ki in slots  ]   )
       #mode tex_id  2 by default
       v= 64 - (v + dv)
       #x1,x2,y1,y2,du,dv = blackwood.fit_area(x1,x2,y1,y2,du,dv,two_side= tex_mirror , ratio =True )
       
       tex_file_id= vob.add_texture_file( dds_name  )       
       tex_id   = vob.set_tex_id( sp1,  vob_name+"@" , shin  ,  tex_file_id,  u,v,du,dv , orie=0 )        
       vob.set_material(  mat_name ,  dc[orient.upper()] , vob_name+"@"   )
 

       
       #vob.set_tex_id( 'Left',  2, 0, 0,0,du,dv,2 )
	   
    if cmd=="SET_TEXTURE_SLOT2":
       sp1= int(li[1])
       vob_name= li[2]
       dds_name= li[3]
       extend=   li[4].upper()
       orient=   li[5].upper()
       if extend == "SINGLE":
           extend=False
       else:
            extend=True       
       slots = [ int(j) for j in li[6:] ]
       #print li
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError
       oid= gl.index( vob_name )
       dc= {"LSIDE":4,"SIDE":3,"TOP":5,"BACK":2,"FRONT":1}
       if not(orient in dc.keys()):
          msg("SET_TEXTURE_SLOT accep only side,top,back,front planes")
          msg("SIDE receive: %s"%(orient ))
       x1,x2,y1,y2 = vob.get_axis_limits( vob_name ,[0,1,2,3,4,5,6,7,8,9] ,dc[orient.upper()] )
       #print "->",x1,x2,y1,y2 
       if extend and dc[orient.upper()] != 3:
          x2 = max( abs(x1),(x2) )
          x1 = -x2          
       mti, nada,nada2 = vob.get_mat_info()
       mat_name =  vob_name +"@"
       if not(mat_name in nada2):
          vob.add_material(   mat_name)       
 
       vob.set_obj_material(oid,mat_name)
       #print "AFTER ->",x1,x2,y1,y2 
       if dc[orient.upper()] == 1 and extend == False:
          px1=x2
          px2=x1
       else:
          px1=x1
          px2=x2 
       vob.set_material_bb(  mat_name, x1,x2,y1,y2)
       tid = vob.get_obj_texid( vob_name )              
       tf,ti,mt= vob.get_mat_pos()
       vi = ti[0] + tid * 24
       shin= vob.data[vi+16 ]+0

        
       tex_mirror= True 
       if dc == 3 : tex_mirror=False
       u,v,du,dv = blackwood.calc_slot( [ int( ki) for ki in slots  ]   )
       #mode tex_id  2 by default
       v= 64 - (v + dv)
       #x1,x2,y1,y2,du,dv = blackwood.fit_area(x1,x2,y1,y2,du,dv,two_side= tex_mirror , ratio =True )
       
       tex_file_id= vob.add_texture_file( dds_name  )       
       tex_id   = vob.set_tex_id( sp1,  vob_name+"@" , shin  ,  tex_file_id,  u,v,du,dv , orie=0 )        
       vob.set_material(  mat_name ,  dc[orient.upper()] , vob_name+"@"   )
 

       
       #vob.set_tex_id( 'Left',  2, 0, 0,0,du,dv,2 )
        
    if cmd=="SET_TEXTURE_SLOT3":
       vob_name= li[1]
       sp1=0
       vob_names =[]
       gl= vob.get_obj_names()

       sj = 1

       print li


       #find extend or single

       valid= False  
       for sk in range(len(li)):
           if li[sk].upper() == "EXTEND" or li[sk].upper() == "SINGLE":
              sj=sk+0
              valid=True             

       vob_names =   li[1:sj-1 ]        

       msg("Found "+" ".join(vob_names) )        
       
       dds_name= li[sj-1]
       orient=   li[sj+1].upper()
       extend=   li[sj].upper()

       #print "SJ=", sj
       #print "DDS_NAME:",dds_name
       #print li
       
       if extend == "SINGLE":
           extend=False
       else:
            extend= True
            
       slots = [ int(j) for j in li[sj+2:] ]
       #print li
       gl= vob.get_obj_names()  
       if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError

       if vob_names ==[]:
          msg("No parts found")
          raise NameError
        
 
       dc= {"LSIDE":4,"SIDE":3,"TOP":5,"BACK":2,"FRONT":1}
       if not(orient in dc.keys()):
          msg("SET_TEXTURE_SLOT accep only side,top,back,front planes")
          msg("SIDE receive: %s"%(orient ))
          
       x1,x2,y1,y2 = vob.get_axis_limits( vob_names[0] ,[0,1,2,3,4,5,6,7,8,9] ,dc[orient.upper()] )
       for vn in  vob_names:
           px1,px2,py1,py2 = vob.get_axis_limits( vn ,[0,1,2,3,4,5,6,7,8,9] ,dc[orient.upper()] )
           x1= min(x1,px1)
           y1= min(y1,py1)           
           x2= max(x2,px2)
           y2= max(y2,py2)
           
       #print "->",x1,x2,y1,y2 
       if extend and dc[orient.upper()] != 3:
          x2 = max( abs(x1),(x2) )
          x1 = -x2          
       mti,nada,nada2 = vob.get_mat_info()
       for vn in  vob_names:
         oid= gl.index( vn)
         tid = vob.get_obj_texid( vn )
         tf,ti,mt= vob.get_mat_pos()
         vi = ti[0] + tid * 24
         shin= vob.data[vi+16 ]+0  #save
         
         mat_name =  vn +"@"
         if not(mat_name in nada2):
            vob.add_material(   mat_name)       
 
         vob.set_obj_material(oid,mat_name)
         #print "AFTER ->",x1,x2,y1,y2 
         vob.set_material_bb(  mat_name, x1,x2,y1,y2)
         tid = vob.get_obj_texid( vn )              
         tf,ti,mt= vob.get_mat_pos()
         vi = ti[0] + tid * 24
         #shin= vob.data[vi+16 ]+0

        
         tex_mirror= True 
         if dc == 3 : tex_mirror=False
         u,v,du,dv = blackwood.calc_slot( [ int( ki) for ki in slots  ]   )
         #mode tex_id  2 by default
         v= 64 - (v + dv)
         #x1,x2,y1,y2,du,dv = blackwood.fit_area(x1,x2,y1,y2,du,dv,two_side= tex_mirror , ratio =True )
       
         tex_file_id= vob.add_texture_file( dds_name  )       
         tex_id   = vob.set_tex_id( sp1, vn+"@" , shin  ,  tex_file_id,  u,v,du,dv , orie=0 )        
         vob.set_material(  mat_name ,  dc[orient.upper()] , vn+"@"   )

         tid = vob.get_obj_texid( vn )
         tf,ti,mt= vob.get_mat_pos()
         vi = ti[0] + tid * 24
         vob.data[vi+16 ]=shin+0

       
       #vob.set_tex_id( 'Left',  2, 0, 0,0,du,dv,2 ) 
	   



    if cmd=="NEW_OBJECT":
        vob_name= li[1]         
        vob.add_object( vob_name, ( 255,255,255 ) ,0  )
         
    if cmd=="WRITE":
        name= li[1]
        msg("WRITE OUT %s"%(name))
        vob.write(name )

        
    if cmd=="SET_COLOR":
        vob_name= li[1]
        shine= li[2].upper()
        rgb= [int(k) for k in li[3:]  ]
        sh= 0
        if shine == "SHINE":
            print "SHINE"
            sh=0
        if shine == "OPAQUE":
            sh=1
            print "OPAQUE"			
              
        gl= vob.get_obj_names()  
        if not(vob_name in gl):
          msg("PART %s NOT FOUND "%(vob_name) )
          raise NameError
        oid= gl.index( vob_name )
        #print blackwood.ss( vob.data[vob.off_obj + oid *16:vob.off_obj + oid *16+4  ]    )      
        vob.data[vob.off_obj + oid *16   ] =rgb[0]
        vob.data[vob.off_obj + oid *16  +1 ] =rgb[1]             
        vob.data[vob.off_obj + oid *16  +2 ] =rgb[2]

              
        tid = vob.get_obj_texid( vob_name )
              
        tf,ti,mt= vob.get_mat_pos()
        vi = ti[0] + tid * 24
        vob.data[vi+16 ]= sh+0
              
          
  #msg("WRITE OUT %s"%(file_output))            
  #vob.write(file_output)


