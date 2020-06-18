#load object
#carrega um OBJ seprando por materiais, para uma struct
import math


def znormal(p1,p2,p3):
    d1=p3[0]-p1[0],p3[1]-p1[1],p3[2]-p1[2]
    d2=p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]
    x=d1[1]*d2[2]- d1[2]*d2[1]
    y=d1[0]*d2[2]- d1[2]*d2[0]
    z=d1[1]*d2[0]- d1[0]*d2[1]
    nnz= math.sqrt( x*x+y*y+z*z)

    if nnz==0: nnz =1.0
    #nnz=1.0
    return x/nnz,y/nnz,z/nnz


def bin_v_h(x,y,z):
        s=  (struct. pack("iii",x*65536.0,y*65536.0,z*65536.0))
        return [ ord(i) for i in s]
    
def similar_v(xyz1,xyz2,pr=0.01):
    if abs(xyz1[0]-xyz2[0])>pr: return False
    if abs(xyz1[1]-xyz2[1])>pr: return False
    if abs(xyz1[2]-xyz2[2])>pr: return False
    return True

def vo_replace_get(vbase,vmod,bin):     

    
    v1=read_obj(vbase)
    v2=read_obj(vmod)
    for i in range(len(v1)):
        if similar(v1[i],v2[i])==False:
            print v1[i], "->",v2[i]
    print v1    


def read_obj(fname):
  #f=open("../beetle/VW new Beetle Polizei.obj","r")
  f=open(fname,"r")
  vtx=[]
  nv=[]
  fc=[]
  obj=[ ] #[ material_name,[(xyz,xyz,xyz)] ]
  lns= f.readlines()
  i=0
  while i < len(lns):
    #print lns[i]
    if len(lns[i])>3: 
      if lns[i][-2]=="\\" :
         #print lns[i] 
         lns[i]=lns[i][0:-2]+lns[i+1]
         del lns[i+1]
         i-=1
    i+=1
         
  
  for l in lns:
    if l[0]!='v' : continue 
    ls=l.split()
    if len(ls)==0: continue
    if ls[0]=='v':
       v,x,y,z =l.split()       
       x,y,z=[float(k) for k in [x,y,z]]
       vtx.append((x,y,z) )
       #print x,y,z
  print "read ",len(vtx), "  vertices"     
  return vtx

def read_obj_faces_names(fname):
  f=open(fname,"r")
  vtx=[]
  nv=[]
  fc=[]
  
  uv=[]  
  fuv=[]
  
  obj=[ ] #[ material_name,[(xyz,xyz,xyz)] ]
  gr= {}
  gr_uv={}
  gr_atc= "DEFAULT"
  gr[gr_atc] = [ ]
  gr_uv[gr_atc] = [ ]  
  lns= f.readlines()
  i=0
  while i < len(lns):
    #print lns[i]
    if len(lns[i])>3: 
      if lns[i][-2]=="\\" :
         #print lns[i] 
         lns[i]=lns[i][0:-2]+lns[i+1]
         del lns[i+1]
         i-=1
    i+=1
         
  print len(lns)
  for l in lns:
    #if l[0]!='v' : continue 
    ls=l.split()
    if len(ls)==0: continue
    if ls[0]=='vt':
       v,x,y,z =l.split()       
       x,y,z=[float(k) for k in [x,y,z]]
       uv.append((x,y,z) )

       
    if ls[0]=='v':
       v,x,y,z =l.split()       
       x,y,z=[float(k) for k in [x,y,z]]
       vtx.append((x,y,z) )
       #print x,y,z
  #print "read ",len(vtx), "  vertices"     
  #return vtx
##       
##    if ls[0]=='vn':
##       v,x,y,z =l.split()
##       x,y,z=[float(k) for k in [x,y,z]]
##       nv.append((x,y,z ) )
    if ls[0]=='g':
       #encontra todos os vertices usados
       if len(ls) == 1:
              print "Object no named found"
              ls.append("DEFAULT")
       #print l
       gr_atc= ls[1]
       gr[gr_atc] = [ ]
       gr_uv[gr_atc] =[ ]
       fc=[]
       
    if ls[0]=='f':
       fcs=ls[1:]
       vi=[ int(k.split("/")[0])-1 for k in fcs]

       
       if len(uv)>0:
         if len(fcs[0].split("/"))>1:          
           uvi=[ int(k.split("/")[1])-1 for k in fcs ]
         else:
           uvi = (1,1,1,1,1,1)  
         for i in range(2,len(uvi)):             
               gr_uv[gr_atc].append( [ uv[uvi[0]],  uv[uvi[i-1]], uv[uvi[i] ] ])
 

             
##       if obj==[]:
##          obj.append(["DEFAULT",[]])
##          print obj   
##       oi=obj[-1][1]
         
       vi=[ int(k.split("/")[0])-1 for k in fcs ]
       for i in range(2,len(vi)):               
           gr[gr_atc].append( [ vi[0],vi[i-1],vi[i] ] )
 

           
  return vtx, gr , gr_uv

##       try:
##          ni=[ int(k.split("/")[-1])-1 for k in fcs]
##       except:
##          print l
##          return None
##       #print vi, ni
##       for i in range(2,len(vi)):
##           p1,p2,p3= vtx[vi[0]],vtx[vi[i-1]],vtx[vi[i] ]
##           n1,n2,n3= nv[ni[0]] ,nv[ni[i-1]],nv[ni[i] ]
##           #print n1,n2,n3
##           #verifica a normal
##           ns=znormal(p1,p2,p3)
##           if n1[0]*ns[0] +n2[1]*ns[1]+n3[2]*ns[2]>0:
##                 oi.append( (p1,p2,p3 ) )
##           else:
##                 oi.append( (p3,p2,p1 ) )  
##       
##    if ls[0]=='usemtl':
##       #novo objeto
##       obj.append([ls[1],[] ])
##       print obj[-1]
    
def read_obj_faces_names_x(fname):
    a,b,c = read_obj_faces_normals(fname)
    return a,b

        
def read_obj_faces_normals(fname):
  #f=open("../beetle/VW new Beetle Polizei.obj","r")
  f=open(fname,"r")
  vtx=[]
  nv=[]
  fc=[]
  vnn=[]
  vfn=[]
  uv=[]
  fuv=[]
  obj=[ ] #[ material_name,[(xyz,xyz,xyz)] ]
  lns= f.readlines()
  i=0
  while i < len(lns):
    #print lns[i]
    if len(lns[i])>3: 
      if lns[i][-2]=="\\" :
         #print lns[i] 
         lns[i]=lns[i][0:-2]+lns[i+1]
         del lns[i+1]
         i-=1
    i+=1
         
  print len(lns)
  for l in lns:
    #if l[0]!='v' : continue 
    ls=l.split()
    if len(ls)==0: continue
    if ls[0]=='v':
       v,x,y,z =l.split()       
       x,y,z=[float(k) for k in [x,y,z]]
       vtx.append((x,y,z) )

       
    if ls[0]=='vt':
       v,x,y,z =l.split()       
       x,y,z=[float(k) for k in [x,y,z]]
       uv.append((x,y,z) )

       
    if ls[0]=='vn':
       v,x,y,z =l.split()       
       x,y,z=[float(k) for k in [x,y,z]]
       normz=  math.sqrt(x*x + y*y +z*z)
       if normz ==0 :
            vnn.append((0,0,1) )    
       vnn.append((x/normz,y/normz,z/normz ) )       
       #print x,y,z
  #print "read ",len(vtx), "  vertices"     
  #return vtx
##       
##    if ls[0]=='vn':
##       v,x,y,z =l.split()
##       x,y,z=[float(k) for k in [x,y,z]]
##       nv.append((x,y,z ) )
    #if ls[0]=='g':
       #print ls     
    if ls[0]=='f':
       fcs=ls[1:]
       vi=[ int(k.split("/")[0])-1 for k in fcs]
       
       ni=[ int(k.split("/")[-1])-1 for k in fcs]
       
##       if obj==[]:
##          obj.append(["DEFAULT",[]])
##          print obj   
##       oi=obj[-1][1]
         
       vi=[ int(k.split("/")[0])-1 for k in fcs ]
       if len(uv)>0:
         uvi=[ int(k.split("/")[1])-1 for k in fcs ]       
         for i in range(2,len(uvi)):
             fuv.append( [ uv[0],uv[i-1],uv[i] ] )         

       
       for i in range(2,len(vi)):
           fc.append( [ vi[0],vi[i-1],vi[i] ] )         
           vfn.append( znormal(vtx[ vi[0]],  vtx[ vi[i-1]], vtx[i] )  )
                      
  return vtx,fc,vfn,fuv

##       try:
##          ni=[ int(k.split("/")[-1])-1 for k in fcs]
##       except:
##          print l
##          return None
##       #print vi, ni
##       for i in range(2,len(vi)):
##           p1,p2,p3= vtx[vi[0]],vtx[vi[i-1]],vtx[vi[i] ]
##           n1,n2,n3= nv[ni[0]] ,nv[ni[i-1]],nv[ni[i] ]
##           #print n1,n2,n3
##           #verifica a normal
##           ns=znormal(p1,p2,p3)
##           if n1[0]*ns[0] +n2[1]*ns[1]+n3[2]*ns[2]>0:
##                 oi.append( (p1,p2,p3 ) )
##           else:
##                 oi.append( (p3,p2,p1 ) )  
##       
##    if ls[0]=='usemtl':
##       #novo objeto
##       obj.append([ls[1],[] ])
##       print obj[-1]
 
#vo_replace_get("../dumb.obj","../tmp2.obj",[]   )              
##gv,gf=read_obj_faces("../teto.obj" )    
##print len(gv)
##print gv[3],gf[3]
