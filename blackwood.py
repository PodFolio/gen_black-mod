#blackwood_mod_tool

import Image, ImageDraw
import os
import os.path

import random

#fmask= 126*256 + 255
fmask= 63*256 + 255 #16383

def to_word(x):
            if x > 65536: print "OVERFLOW \n\n\n" 
            return x&0xff, (x&0xff00)/256
def toname(d,fill=False):
    s=""
    for k in d:
        if k==0:
           if fill:
              s+=" "  
           else:
              return s 
        else:
            cs=chr(k)
            if cs==" ":
                s+="_"
            else:    
               s+=chr(k)
            
    return s
def ss(g,x=3):
    s=""
    for i in g:
        if x==3:
          s+="%03i "%(i)
        if x==5:s+="%5i "%(i)
    return s


def fixed(sd):
    #print "FIX", sd
    s= chr( sd[0]) + chr(sd[1]) +chr( sd[2]) +chr( sd[3]) 
    return  (struct.unpack("i",s)[0])/65536.0
def bin_vd(d,x,y,z):
            s=  (struct. pack("iii",x*65536.0,y*65536.0,z*65536.0))
			#s=  (struct. pack("iii",(x/60000)*65536.0,(y/60000)*65536.0,(z/60000)*65536.0)) jak z 3dsa grid 10000
            return [d,0,0,0]+[ ord(i) for i in s]

def read_axyz(d):
                   vi=0
                    
                   s=fixed(d[vi:vi+4 ]);vi+=4
                   x=fixed(d[vi:vi+4 ]);vi+=4
                   y=fixed(d[vi:vi+4 ]);vi+=4
                   z=fixed(d[vi:vi+4 ]);vi+=4
                   return [s,x,y,z]


def fit_area(x1,x2,y1,y2,du,dv, two_side=True, ratio =True ):
    if  two_side and x1*x2 > 0:
        limit = max(abs(x1),abs(x2)) 
        x1,x2 = -limit, +limit 
        
    if  two_side==False and x1*x2 < 0:
        limit = max(abs(x1),abs(x2))
        if x1 > 0 :
           x1,x2 = 0.001,+limit 
        else:
           x1,x2 = -limit,-0.001
           
    dx,dy = x2-x1 , float(y2-y1)       
    ajust=True
    nin= 0
    sx = du/dx
    sy=  dv/dy

    
    
    if   ajust:
      du1 =  dx * sx
      dv1 =  dy * sx
      if not(du1 > du or dv1 > dv): 
         du, dv = du1,dv1
      else:    
        du2 =  dx * sy
        dv2 =  dy * sy          
        if not(du2 > du or dv2 > dv): 
         du, dv = du2,dv2

    print "ratio", du/dx ,dv/dy
      
    return x1,x2,y1,y2,du,dv 

    
def calc_slot(sl, ori=0 ):
    u,v,du,dv=[],[],[],[]
    
    for s in sl:
        j,i= int(s/4), s%4

        u.append( i*16 )
        v.append( j*16 )
        du.append( (i+1)*16 )
        dv.append( (j+1)*16 )
        
    return min(u),min(v) , max(du)-min(u) ,   max(dv)-min(v)  

def find_header(data,voff):
    i=voff -1
    # suponha que este o numero de vertices esta em vs+30
    start=False

    dsz= len(data)
    while start==False:
        start=True
        i+=1
         
        if i+3 > len(data):
             return None,None
            
        nv=data[i] + data[i+1]*256
        nf=data[i+2] + data[i+3]*256           
        mn=data[i+30]  # offset 60
        off_obj= i+32  # offset 62
        off_vi=  off_obj + 16*mn
        off_fc=  off_vi + 16* nv
        face_end= off_fc + nf*12

        if face_end > dsz or off_vi > dsz or  off_fc > dsz:
 
           start =False
        if start==False: continue  
            
        if  mn<1  or nv <2 or nf < 9    : #if  mn<1  or nv <3 or nf < 9    :
  
            
            start=False
            continue
        
        if start==False: continue
        
 
        
        #testa os objetos, cada objeto deve ter a primeira letra valida
        #print "--------------------------"
        for k in range(mn):
            for s in range(1):
              name= data[off_obj +4 + 16*k  + s  ]
              if  name < 20 and name >0 :
 
                  start=False
       
                  break
                  pass
            if start==True:
               #print toname( data[off_obj+4 + 16*k :  off_obj+4 + 16*(k+1) ] )
               pass
        if start==False: continue



 
        
        #testa os vertices
        
        for k in range(nv):  
            kv= k*16 + off_vi
            a,x,y,z= read_axyz(data[kv :kv +16])
            if   data[kv+2]>0 or data[kv+3]>0 :
 
               start=False
               break
            
 
            
        for k in range(nf):
            kf= k*12 + off_fc
            
            if data[kf+2] > mn  or   data[kf+10]+256*(data[kf+11] & 0x1f  )> nf     :
 
               start=False
               break                
            
        if start==False: continue
 
        tex_off=face_end+0
        while data[tex_off]==0:  tex_off +=1
        
        num_tex=data[tex_off]
        tex_off+=4
        vi= tex_off +0
        for j in range(num_tex):
            skp_name=data[ tex_off + 20 * j +4 ]
            if skp_name <20 or skp_name>150:
                  start=False
                  #break
                  
            #print toname(  data[ tex_off + 20 * j +4 :tex_off + 20 * (j+1) +4  ]    ) 
            vi+=20
            #if start==False:        continue
            
        ktex_num= data[vi] +256*  data[vi+1]
        vi+=4
         
        for j in range(ktex_num):              
              vi+=24
              
        num_mat=data[vi]
        vi+=4
        for j in range(num_mat):
            mat_name=data[vi:vi+15]
            #print toname( mat_name )
            vi+=44
 
        return i,vi

    print "OUT",i    


    

import struct
import math    
from  objread import *

class blk_file:
   def load(self,fname):
    self.data = []
    self.mid=1 
    self.offset=0
    f=open(fname,'rb')   
    buf=None

    buf=f.read(4096)
    while buf!="":
         for s in buf:
            self.data.append(struct.unpack("B",s)[0])
         buf=f.read(4096)
    self.data.append(struct.unpack("B",s)[0])
    self.set_mid(1)
    

   def set_mid(self,mid):
       n=mid+0
       vprox=0
       vnext=0
       while n >0:
         n=n-1
         ss= find_header(self.data,vprox )
         print ss
         if ss[0] ==None:
            print "MESH OUT OF RANGE !" 
            raise IndexError
            
         vnext, vprox = ss
       self.mid=mid+0  
       self.offset= vnext
       self.update_geo_num()
       self.vfree={}
       #self.scan_vertex()
           


   def  scan_normals(self, obj_id , q= 0.404 ):
        import math
        #make some things.
        
        def vertex_same(s1,s2):
            k=0 
            k+= min(s2.count( s1[0] ),1)
            k+= min(s2.count( s1[1] ),1)
            k+= min(s2.count( s1[2] ),1)           
            #if k>0 : print k, s1,s2  
            return k
            
        def znormal(v1,v2,v3):
            a,x1,y1,z1= self.get_vertex(v1) 
            a,x2,y2,z2= self.get_vertex(v2)
            a,x3,y3,z3= self.get_vertex(v3)
            v1 = x2-x1, y2-y1 , z2-z1
            v2 = x3-x2, y3-y2 , z3-z2            
            nx,ny,nz =  v1[1] * v2[2] - v1[2] * v2[1], v1[2] * v2[0] - v1[0] * v2[2], v1[1] * v2[0] - v1[0] * v2[1]
            nn= math.sqrt(nx*nx+ny*ny+nz*nz)
            if nn > 0:
               return nx/nn,ny/nn,nz/nn
            return 1,0,0

        def dot(a,b):
            return a[0]*b[0] + a[1]*b[1]+ a[2]*b[2]      
        sss=[]    
        fvi =[]
        nv=[]
        viz=[]
        valid=0
        for j in range(self.nf):            
         
            nv.append([])
            fvi.append([])
            viz.append([])
            fii= self.off_fc + j*12  
            if self.data[fii+2] != obj_id  or  self.data[fii+4]>0  or self.data[fii+1]!=4  :
                 continue                  
            k1= self.data[fii+6] + 256* self.data[fii+7]
            k2= self.data[fii+8] +  256* self.data[fii+9]
            k3= self.data[fii+10] + 256*  self.data[fii+11]
        
            if k1 > self.nv or  k2 > self.nv  or k3 > self.nv : continue
            
            nv[j] =znormal(k1,k2,k3)  
            fvi[j]=[ k1+0,k2+0,k3+0] 
            valid+=1
        nviz=0
 
        for fi in range( self.nf  ):            
            if fvi[fi]==[]: continue
            
            for fj in range(fi+1, self.nf ):
                 if fvi[fj]==[]: continue  
                 if  vertex_same( fvi[fi], fvi[fj] )>0 :
                     if dot(nv[fi],nv[fj]) > q   :
                         viz[fi].append( fj+0 )
                         viz[fj].append( fi+0 )
                         
            if viz[fi]==[]: nviz+=1
                   
         
        
   
        gr=[]
        ungr=[]
        for j in   range( self.nf ):             
            if fvi[j]!=[]:
                ungr.append( j+0 )
            else:
                continue
        print "len :", valid , len(ungr)      
        while ungr!=[]:
            seed= ungr[0] 
            tgr=[ seed+0] 
            #ungr.remove( seed+0 ) 
            uck=[ seed+0 ]
            tail=0
            c=True 
            while tail < len(tgr) :
                
                fi =tgr[tail]
                
                for fj in ungr:
                        if   tgr.count(fj)>0 :
                           continue
                        if fvi[fj] ==[]:
                           continue
                        #sv=vertex_same( fvi[fi], fvi[fj] )
                        sv = viz[fi].count(fj)
                        if  sv>0:
                              #print "add " ,fj
                              tgr.append(fj)
                tail+=1                               

                        
            gr.append(tgr+[])                                 
            #print tgr   
            for k in  tgr :
                ungr.remove(k)

                
        #for k in gr:
            #print k
                        
        gid = [1 for i in gr ]
        sh = [ [] for i in gr  ]
        for i in range(len(gr)):
          for j in range(i+1, len(gr)):               
              for fi in gr[i]:
                for fj in gr[j]:                  
                   if vertex_same( fvi[fi], fvi [fj] )>0:
                      if gid[ i ] ==gid[ j ]:
                         gid[ j ] = gid[ i ] +1
                         sh[i].append(j+0)
                         sh[j].append(i+0)
                         break
                    
          print "group ",i," has id", gid[i] , "  share ",sh[i]       
        for i in range(len(gr)):             
            for fi in gr[i] :
               self.data[ 12* fi  + self.off_fc +5  ]= gid[i] #ajust normal group

            
   def  scan_vertex(self):       
        for j in range(self.nv):  self.vfree[j]=0
        for j in range(self.nf):
           fi= self. off_fc + j*12
           k1= self.data[fi+6] + 256* self.data[fi+7]
           k2= self.data[fi+8] +  256* self.data[fi+9]
           k3= self.data[fi+10] + 256*  self.data[fi+11]            

           for kv in (k1,k2,k3):
               k = kv &fmask    
               if k < self.nv:
                      self.vfree[k]+=1
             
            
   def  update_geo_num(self):
        i= self.offset         
        self.nv=self.data[i] + self.data[i+1]*256
        self.nf=self.data[i+2] + self.data[i+3]*256           
        self.mn=self.data[i+30]  # offset 60
        self.off_obj = i+32
        self.off_vi=  self.off_obj + 16*self.mn
        self.off_fc=  self.off_vi + 16* self.nv

        if self.nv >= fmask:
           raise OverflowError,"Number of vertex is too hight"
 
        
   def get_obj_material_id( self, obj_name ):
       l=self.get_obj_names()
       j= l.index( obj_name ) 
       mid=   self.data[self.off_obj+j*16+14]   +   256*self.data[self.off_obj+j*16+15 ]


       return mid

    
   def get_obj_material( self, obj_name ):
       mid= self.get_obj_material_id(obj_name)
       tf,ti,mt= self.get_mat_info()

       return mt[mid]


   def dump_mesh_as_string( self   ):
       so=[]
       self.update_geo_num()
       
       for i in range(self.nv):
           vi= self.off_vi + i *16
           a,x,y,z= read_axyz(self.data[vi:vi+16])
           #print a,x,y,z
           
           so.append( "v  %f %f %f \n"%(x,y,z ) )
           
       for name in  self.get_obj_names():
           for model in range(0,9):
               fl= self.get_face_list( name, [model+0] )
               
               if len(fl) >0:
                  so.append("g m%i_%s \n"%( model, name) ) 
                  for fj in fl:
                     if self.data[ fj*12 + self.off_fc +1 ]!=model :
                        continue 
                     v1,v2,v3= self.get_triangle_index( fj )
                     v1= v1 &fmask
                     v2= v2 &fmask
                     v3= v3 &fmask                     
                     if v1 < self.nv  and   v2 < self.nv  and v3 < self.nv  :
                        so.append("f %i %i %i \n"%(v1+1,v2+1,v3+1))
       return so  

   
   def get_obj_names(self ):
       lst=[]
       for j in range(self.mn):
         oz= self.data[self.off_obj+j*16:self.off_obj+j*16+16 ]
         #print oz
         RGBA=oz[0:4]
         RGBA=[g/256.0 for g in oz[0:4]]
         lst.append( toname(oz[4:16]) )
       return lst  

         
   def add_vertex(self ):
  
       self.update_geo_num()
       i= self.offset
       for j in range(16):self.data.insert( j+ self.off_vi + (self.nv ) *16 ,0  )
       
       self.data[i],self.data[i+1] = to_word(self.nv+1)
       self.update_geo_num()
       vi = self.nv-1
       #self.set_vertex(  vi , 0,0,0)
       return vi
       
   def get_vertex(self,k):
        self.update_geo_num()
        if k > self.nv:            
           kv= (k & fmask )*16 + self.off_vi
        else:
           kv= k *16 + self.off_vi
        a,x,y,z= read_axyz(self.data[kv:kv +16])
        
        a= self.data[kv ]
        return a,x,y,z    


            
   def set_vertex(self, i ,  x,y,z,a=1,tol=0.01):       
       vdata= bin_vd(a,x,y,z)
 
           
       for j in range(0,4):   self.data[j+ self.off_vi + i*16] = 0
       for j in range(4,16):  self.data[j+ self.off_vi + i*16]= vdata[j]
       
       self.data[ self.off_vi + i*16] = a 
       if abs(x) < tol:
          self.data[ self.off_vi + i*16]=  2          
       else:
          self.data[ self.off_vi + i*16] = 1
          

   def get_obj_file_texture(self, name):
       texid= self.get_obj_texid(name)
       mtf,mti,mmt= self.get_mat_info()
       tf,ti,mt= self.get_mat_pos()


       vi = ti[0] + 24* texid 
       return   mtf[ self.data[vi+18]]

   def set_obj_material(self,oid,mat_name):
        self.update_geo_num()
        mat_id=  self.get_mat_info()[2].index(mat_name)
        
        self.data[self.off_obj+ oid*16+14], self.data[self.off_obj+ oid*16 +15]= to_word( mat_id  )
        
       
   def add_object(self, name, rgb, mat_id):
        self.update_geo_num()
        i= self.offset         
        self.nv=self.data[i] + self.data[i+1]*256
        self.nf=self.data[i+2] + self.data[i+3]*256           
        self.mn=self.data[i+30]  # offset 60
        self.off_obj = i+32

         
        self.off_vi=  self.off_obj + 16*self.mn
        self.off_fc=  self.off_vi + 16* self.nv
        
        for j in range(16):
            self.data.insert( self.off_vi,0 )
        self.data[i+30] =self.mn + 1
        
        
        self.update_geo_num()
        oid= self.data[i+30]-1
        
        for j in range(min(10 ,len(name)) ):
            self.data[self.off_obj+ oid*16+j+4] =ord(name[j])
            
        self.data[self.off_obj+ oid*16]=rgb[0]
        self.data[self.off_obj+ oid*16+1]=rgb[1]
        self.data[self.off_obj+ oid*16+2]=rgb[2]

        self.data[self.off_obj+ oid*16+14], self.data[self.off_obj+ oid*16 +15]= to_word( mat_id  )
        
   def add_face(self):
        self.update_geo_num()
        i= self.offset
 

        self.data[i+2],self.data[i+3] = to_word( self.nf+1)
        self.update_geo_num()

        
        for j in range(12):
           self.data.insert( j+self.off_fc + (self.nf-1) *12 ,0  )
        
        return self.nf-1
    
   def  delete_faces_col( self, vob_name  ) :
        self.update_geo_num() 
        oi= self.get_obj_names().index(vob_name)
        for j in range(self.nf-1,-1,-1):
            if self.data[ 12*j+self.off_fc + 2] == oi and  self.data[ 12*j+self.off_fc + 4] ==2:
              self.delete_face( j)   
               
        
   def delete_face(self,k ):
        self.update_geo_num()
        if k >= self.nf:
            raise IndexError
            return
 
        i= self.offset
 
        fi= self.off_fc + k*12
##        k1= self.data[fi+6] + 256* self.data[fi+7]
##        k2= self.data[fi+8] +  256* self.data[fi+9]
##        k3= self.data[fi+10] + 256*  self.data[fi+11]
##        for kv in (k1,k2,k3):
##            kv =kv  & fmask
##            if kv < self.nv:
##               self.vfree[ kv] -=1
               
        del  self.data[  self.off_fc + k*12:self.off_fc + k*12+12 ]
        self.data[i+2],self.data[i+3] = to_word( self.nf-1)
        self.update_geo_num()  
          

              
         
   def set_face_type(self, i , tipo):
            self.update_geo_num() 
            fi= self.off_fc + i*12
            self.data[fi+4]= tipo
            
   
   def  set_face( self,  i , vv1,vv2,vv3 , obj_id , mirror ,model=0  ,  aid= 0 ):
            self.update_geo_num() 
            fi= self.off_fc + i*12
            k1= self.data[fi+6] + 256* self.data[fi+7]
            k2= self.data[fi+8] +  256* self.data[fi+9]
            k3= self.data[fi+10] + 256*  self.data[fi+11]
            for k in (k1,k2,k3):
               if k < self.nv:                   
                      self.vfree[k] -= 1
  
                       
            for k in (k1,k2,k3):
               if k < self.nv:                              
                  self.vfree[k]+=1
 
            
            fd=[0 for j in range(12)]
            fd[0]=1
            if mirror ==0: #off
                fd[0]=16
            elif mirror ==1: #on
                fd[0]=1
            elif mirror ==2: #fix
                fd[0]=0
            elif mirror ==3: #glass
                fd[0]=4
            elif mirror ==4: #fix2
                fd[0]=2
            elif mirror ==5: #fix3
                fd[0]=8				

                
            if  mirror==2 : 
                self.data[self.off_vi+ 16*vv1] = 0
                self.data[self.off_vi+ 16*vv2] = 0
                self.data[self.off_vi+ 16*vv3] = 0
                
            

        
                
            fd[1]=model
            fd[2]=obj_id
            if mirror!=1:
				fd[3]=1    #Type

            fd[4]=aid+0 #Colision
            if mirror==3:
				fd[5]=3    #Smooth

            fd[6],fd[7]=to_word(vv1)
            fd[8],fd[9]=to_word(vv2)
            fd[10],fd[11]=to_word(vv3)
            
            for j in range(12):
                self.data[ j+ fi ]=  fd[j]           
            

   
   def add_material( self, base_name):
       tf,ti,mt= self.get_mat_pos()

       for i in range(44):
           self.data.insert( mt[0]+ mt[1]*44, 0 )
       for i in range(min(10,len(base_name))):
           self.data[ mt[0]+ mt[1]*44+  i] = ord( base_name[i] )
           
       self.data[mt[0]-4 ],self.data[mt[0]-3 ] = to_word( mt[1]+1  )
       
       

    
   def add_texture_file(self,file_name):
       #verifica se existe e devolve
       tf,ti,mt= self.get_mat_pos()
       vi=tf[0]
       for j in range(tf[1]):
           tex_nome=toname(self.data[j*20+  vi+4: j*20+  vi+20])
           if tex_nome == file_name: return j   
       pass
       tf,ti,mt= self.get_mat_pos( )    
       self.data[tf[0]-4 ],self.data[tf[0]-3 ] = to_word( tf[1]+1  )

       fp = [0 for i in range(20) ]
       for i in range(min(len(file_name), 15) ): 
          fp[i+4] =ord(file_name[i])
       for k in range(20):  
           self.data.insert( tf[0] +  tf[1]* 20 +k, fp[k])
       self.update_geo_num()
       return tf[1]



   def get_orient_obj(self, name):
       mat_name= self.get_obj_material(   name )
       
       mat= self.get_material_id( mat_name )       
       tf,ti,mt= self.get_mat_pos()
       vi= mt[0]+mat*44       
       pori= self.data[vi+16 ]

       return pori


   def  get_texture_slot_size(self, tex_id):

       tf,ti,mt= self.get_mat_pos()
       vi = ti[0] + tex_id * 24        
       print  ss(range(24))       
       print  ss(self.data[vi:vi+24 ])

       
       duv=  float(self.data[vi+ 20 ]), float(self.data[vi +21 ])
       uv = float(self.data[vi +22 ]), float(self.data[vi+ 23 ] )
       uflag= self.data[vi  +17 ]
       

       return duv[0],duv[1]


   def  get_xyzuf_list( self, obj_name , model  ,kside =0  ):

       xyzuv=[]
       
       size=1.0
       dss= size/64.0
       
       obj_id  =  self.get_obj_names().index(obj_name )

       
       mat_name= self.get_obj_material(  obj_name ) 
       x1, x2,y1,y2= self.get_material_bb( mat_name  )
 
       if x1*x2 < 0 :
           mirror =True
       else:
           mirror= False
       
       mat= self.get_material_id( mat_name )       
       tf,ti,mt= self.get_mat_pos()
       vi= mt[0]+mat*44       
       pori= self.data[vi+16 ]
       
       tex_id= self.data[vi+36   ]  
 
          
       vi = ti[0] + tex_id * 24
        
        
       duv=  float(self.data[vi+ 20 ]), float(self.data[vi +21 ])
       uv = float(self.data[vi +22 ]), float(self.data[vi+ 23 ] )
       uflag= self.data[vi  +17 ]
 
       
       tf,ti,mt= self.get_mat_pos()
       vm= mt[0]+mat*44
 
       
       def get_uv( x,y , uf=1  ):
                dx = (x - x1)/float(x2-x1)
                dy = (y - y1)/float(y2-y1)
                #print dx,dy
                
                ku=dx* duv[0] + uv[0]
                kv=dy* duv[1] + uv[1]
                
                if uf==0:
                   ku= (dx)* duv[0] + uv[0]
                   kv= 64-(dy* duv[1] + uv[1])

                if uf==1: 
                   ku= 64  -  (dy*duv[1] + uv[1])
                   kv= 64  -  (dx*duv[0] + uv[0])

                   
                if uf==2:
                   ku=dx* duv[0] + uv[0]
                   kv=dy* duv[1] + uv[1]
                   kv =64- kv
                   
                if uf==3:
                   ku=dx* duv[0] + uv[0]
                   kv=dy* duv[1] + uv[1]
                   kv,ku= ku,kv
                   
                if uf==4:
                   ku=(dx)* duv[0] + uv[0]
                   kv=dy* duv[1] + uv[1]                   
                   ku = 64-(dx * duv[0]+uv[0])
                   kv = 64-(dy * duv[1]+uv[1])
               
                return ku * dss,kv*dss
            
 
       sside=1.0

       xflip=1.0

       if kside >0:
          sside=-1.0 
       
       repeat=True
       while repeat:
         for j in range( self.nf):
 
            fii= self.off_fc + j*12  
            if self.data[fii+2] != obj_id  or  self.data[fii+4]>0  or self.data[fii+1]!=model  :
                 continue

            if self.data[fii]!=1 and sside < 0 :
               continue
            
           
            if self.data[fii]==16:
                xflip = -1.0
            else:
                xflip=   1.0

 
                
            
            
            k1= self.data[fii+6] +  256*self.data[fii+7]
            k2= self.data[fii+8] +  256*self.data[fii+9]
            k3= self.data[fii+10] + 256*self.data[fii+11]




            
            v1= self.get_vertex(k1) 
            v2= self.get_vertex(k2)
            v3= self.get_vertex(k3)
            
            #if v1[0] & 1 ==0  or v2[0] & 1 ==0 or v3[0] & 1 ==0 :
            #    continue

            
            u,v = 1,2
            if pori == 5:
               u,v=  1,2
            elif pori == 3:
               u,v=  2,3
            elif pori == 2:               
               u,v=  1,3
            elif pori == 1:               
               u,v=  1,3
            elif pori == 4:               
               u,v=  2,3


               
            fv1 ,fv2 ,fv3  = [ [vk[0],sside*xflip*vk[1],vk[2],vk[3]]   for vk in (v1,v2,v3)]
             
            is_v= True
            for vk in (fv1,fv2,fv3):
              if vk[u] < x1 or vk[u] > x2 or    vk[v] < y1 or  vk[v] > y2  :
                  #is_v=False
                  pass

             
            if  is_v:
                 for vj in (fv1,fv2,fv3):
                    
                   puv = get_uv( vj[u],vj[v],uflag   ) 
                   xyzuv.append( [ vj[1],vj[2],  vj[3],  puv[0],puv[1] ]  )
                 
                 #render the poligon
                 #draw.line( puv[0] + puv[1], fill=(255,255,255) ) 
                 #draw.line( puv[1] + puv[2], fill=(255,255,255) )             
                 #draw.line( puv[2] + puv[0], fill=(255,255,255) )
     
         repeat=False
       return  xyzuv
       

   
   def render_template(self, obj_id, model ,image_name, size=4096 ,   kside=   0):
       #lets find this file
       
       if os.path.exists(image_name):
          img= Image.open(image_name)
       else:
          img= Image.new("RGBA", [size,size], (255, 255, 255, 0) )
       draw= ImageDraw.Draw(img )   
       obj_name= self.get_obj_names()[obj_id]

       dss= size/64.0 
       
       mat_name= self.get_obj_material(  obj_name ) 
       x1, x2,y1,y2= self.get_material_bb( mat_name  )
       print obj_name
       print x1,y1,x2,y2
       if x1*x2 < 0 :
           mirror =True
       else:
           mirror= False
       
       mat= self.get_material_id( mat_name )       
       tf,ti,mt= self.get_mat_pos()
       vi= mt[0]+mat*44       
       pori= self.data[vi+16 ]
       
       tex_id= self.data[vi+36   ]  
 
          
       vi = ti[0] + tex_id * 24
        
        
       duv=  float(self.data[vi+ 20 ]), float(self.data[vi +21 ])
       uv = float(self.data[vi +22 ]), float(self.data[vi+ 23 ] )
       uflag= self.data[vi  +17 ]

       
       #print  ss(range(24))       
       #print  ss(self.data[vi:vi+24 ])
       
       tf,ti,mt= self.get_mat_pos()
       vm= mt[0]+mat*44
       
       #print  ss(self.data[vm:vm+24 ])
       
       
       #print  ss(self.data[ti[0] + tex_id * 24 : ti[0] + (tex_id+1) * 24  ])
       
       def get_uv( x,y , uf=1  ):
                dx = (x - x1)/float(x2-x1)
                dy = (y - y1)/float(y2-y1)
                #print dx,dy
                
                ku=dx* duv[0] + uv[0]
                kv=dy* duv[1] + uv[1]
                
                if uf==0:
                   ku= (dx)* duv[0] + uv[0]
                   kv= 64-(dy* duv[1] + uv[1])

                if uf==1: 
                   ku= 64  -  (dy*duv[1] + uv[1])
                   kv= 64  -  (dx*duv[0] + uv[0])

                   
                if uf==2:
                   ku=dx* duv[0] + uv[0]
                   kv=dy* duv[1] + uv[1]
                   kv =64- kv
                   
                if uf==3:
                   ku=dx* duv[0] + uv[0]
                   kv=dy* duv[1] + uv[1]
                   kv,ku= ku,kv
                   
                if uf==4:
                   ku=(dx)* duv[0] + uv[0]
                   kv=dy* duv[1] + uv[1]                   
                   ku = 64-(dx * duv[0]+uv[0])
                   kv = 64-(dy * duv[1]+uv[1])

                       
                    
                #print ku,kv                
                return ku * dss,kv*dss
            
 
       sside=1.0

       xflip=1.0

       if kside >0:
          sside=-1.0 
       
       repeat=True
       while repeat:
         for j in range( self.nf):
 
            fii= self.off_fc + j*12  
            if self.data[fii+2] != obj_id  or  self.data[fii+4]>0  or self.data[fii+1]!=model  :
                 continue

            if self.data[fii]!=1 and sside < 0 :
               continue
            
           
            if self.data[fii]==16:
                xflip = -1.0
            else:
                xflip=   1.0

 
                
            
            
            k1= self.data[fii+6] +  256*self.data[fii+7]
            k2= self.data[fii+8] +  256*self.data[fii+9]
            k3= self.data[fii+10] + 256*self.data[fii+11]




            
            v1= self.get_vertex(k1)
            v2= self.get_vertex(k2)
            v3= self.get_vertex(k3)
            
            #if v1[0] & 1 ==0  or v2[0] & 1 ==0 or v3[0] & 1 ==0 :
            #    continue

            
            u,v = 1,2
            if pori == 5:
               u,v=  1,2
            elif pori == 3:
               u,v=  2,3
            elif pori == 2:               
               u,v=  1,3
            elif pori == 1:               
               u,v=  1,3
            elif pori == 4:               
               u,v=  2,3


               
            fv1 ,fv2 ,fv3  = [ [vk[0],sside*xflip*vk[1],vk[2],vk[3]]   for vk in (v1,v2,v3)]
             
            is_v= True
            for vk in (fv1,fv2,fv3):
              if vk[u] < x1 or vk[u] > x2 or    vk[v] < y1 or  vk[v] > y2  :
                  #is_v=False
                  pass

             
            if  is_v:
                 puv= [ get_uv( vj[u],vj[v],uflag   )   for vj in (fv1,fv2,fv3)]
                
                 #render the poligon
                 #draw.polygon( puv[0] + puv[1]+ puv[2],  fill=(155,155,155) )
                 draw.line( puv[0] + puv[1], fill=(0,0,0) ) 
                 draw.line( puv[1] + puv[2], fill=(0,0,0) )             
                 draw.line( puv[2] + puv[0], fill=(0,0,0) )

                       
         repeat=False
         #if mirror and sside >0 :
            #sside=-1 
            #repeat=True
            
       draw.line(  get_uv(x1,y1,uflag )+get_uv(x1,y2,uflag  ) , fill=(0,0,0) ) 
       draw.line(  get_uv(x1,y2,uflag )+get_uv(x2,y2,uflag  ), fill=(0,0,0) )             
       draw.line(  get_uv(x2,y2,uflag )+get_uv(x2,y1,uflag  )  , fill=(0,0,0) )
       draw.line(  get_uv(x2,y1,uflag )+get_uv(x1,y1,uflag  )  , fill=(0,0,0) )
       
       del draw
       img.save(image_name, 'PNG')
       del img

       
   def get_mat_info(self):       
       face_end= self.off_fc + self.nf*12
       tex_off=face_end+0
       out=[[],[],[]]       
       while self.data[tex_off]==0:  tex_off +=1
       num_tex=self.data[tex_off]
       tex_off+=4
       vi= tex_off +0
              
       for i in range(num_tex):
           out[0].append(  toname(self.data[ vi+4 : vi+20]  ))
           vi+=20
                        
       ktex_num= self.data[vi] +256*  self.data[vi+1]       
       vi+=4
       tex_id_off = vi+0
       #out.append([tex_id_off +0, ktex_num+0 ] )       
       for i in range(ktex_num):
          out[1].append( toname(self.data[ vi:  vi +15]))               
          vi+=24
       num_mat=self.data[vi]+0
       vi+=4
       for i in range(num_mat  ):
           out[2].append(  toname(self.data[vi:vi+15]))                
           vi+=44                    
       return out

   def get_face_list_id(self,obj_id, models=[0,1,2,3,4,5,6,7,8,9,10]):      
       #obj_id  = oid.index( name  )       
       out=[]
       for j in range( self.nf):
            fii= self.off_fc + j*12  
            if (self.data[fii+2] == obj_id ) and (self.data[fii+4] ==0 ) and (models.count( self.data[fii+1]) > 0  )    :
                out.append( j +0)   
       return out

    
    
   def get_face_list(self,name, models=[0,1,2,3,4,5,6,7,8,9,10]):
       self.update_geo_num()
       oid = self.get_obj_names( )
       obj_id  = oid.index( name  )       
       out=[]
       sk=0
       sd=0
       for j in range( self.nf):
            fii= self.off_fc + j*12  
            if (self.data[fii+2] == obj_id ) :
                sk+=1
                if (self.data[fii+4] ==0 ):
                   sd+=1        
                   out.append( j +0)
       
       return out
	   
   def face_is_safe(self, fi):
            fii= self.off_fc + fi *12 
            k1= self.data[fii+6] + 256* self.data[fii+7]
            k2= self.data[fii+8] +  256* self.data[fii+9]
            k3= self.data[fii+10] + 256*  self.data[fii+11]
            if k1 >= self.nv or  k2 >= self.nv or k3 >= self.nv:
                return False
            return True
       
   def get_triangle_index(self, fi ):
            fii= self.off_fc + fi *12 
            k1= self.data[fii+6] + 256* self.data[fii+7]
            k2= self.data[fii+8] +  256* self.data[fii+9]
            k3= self.data[fii+10] + 256*  self.data[fii+11]         
            return [  k for k in (k1,k2,k3) ]
        
   def get_axis_limits(self, name,  models , plane ):
       flists= self.get_face_list( name, models)
       u,v = 1,2
       if  plane == 5:
           u,v=  1,2
       elif  plane == 3:
           u,v=  2,3
       elif  plane == 2:               
           u,v=  1,3
       elif  plane == 1:               
           u,v=  1,3
       elif  plane == 4:               
           u,v=  2,3
 
       pu=[]
       pv=[]
       if len(flists) < 1:
           return 0, 0.01,0,0.01
       for fi in  flists :
 
            
           for j in self.get_triangle_index(fi):
               pt = self.get_vertex( j )
               pu.append( pt[u]*1.0 )
               pv.append( pt[v]*1.0 )

               
       x1,x2,y1,y2 = min(pu),max(pu) , min(pv),max(pv)
       
       return x1,x2,y1,y2
   
   def get_mat_pos(self):
       face_end= self.off_fc + self.nf*12
       tex_off=face_end+0
       out=[]       
       while self.data[tex_off]==0:  tex_off +=1
       
       num_tex=self.data[tex_off]
        
       
       tex_off+=4
       vi= tex_off +0
       out.append([tex_off +0, num_tex+0 ] )       
       for i in range(num_tex):vi+=20       
       ktex_num= self.data[vi] +256*  self.data[vi+1]
        
       vi+=4
       tex_id_off = vi+0
       out.append([tex_id_off +0, ktex_num+0 ] )       
       for i in range(ktex_num):vi+=24
       num_mat=self.data[vi]+0
       vi+=4
       out.append([vi +0, num_mat+0 ] )       
       return out

   def get_material_id(self,mat_name):
        a,b,c = self.get_mat_info()
        for k in range(len(c)):
            if c[k]==mat_name:
               return k 
        for k in range(len(c)):
            tmp=c[k].replace(" ","_")
            if tmp==mat_name: return k
        raise NameError    
        return None    

   def get_material_bb( self, mat_name):
       out=[]
       tf,ti,mt= self.get_mat_pos()
       mat= self.get_material_id( mat_name )
       vi= mt[0]+ mat *44       
        
       for k in range(4):
           out.append(  fixed( self.data[vi+20+4*k: vi+20+4*k+4 ] )) 
       return out

           
   def set_material_bb( self, mat_name, x1,x2,y1,y2):
       def bin_nt(x,y,z,w ):
            s= (struct.pack("iiii",x*65536.0,  y*65536.0,z*65536.0,w*65536.0 ))
            return [ ord(i) for i in s]
       tf,ti,mt= self.get_mat_pos() 
       mat= self.get_material_id( mat_name )
       vi= mt[0]+ mat *44       
       tmp =  bin_nt(x1,x2,y1,y2)
       for k in range(16):
           self.data[vi+20+k] = tmp[k]+0

        
   def get_obj_texid(self, vob_name ):
      mat_name=  self.get_obj_material(  vob_name  )
      mat= self.get_material_id( mat_name )
      tf,ti,mt= self.get_mat_pos()
      vi=mt[0]+mat*44       
      return self.data[vi+36 ]+0

      
   def set_material(self, mat_name , orientation, tex_id_name  ):
       #tf,ti,mt= self.get_mat_pos()
       #tex_file= self.add_texture_file( texture_file ) #obtem a id do arquivo
       #u,v,du,dv=calc_slot( tex_slots )
       #tex_id= self.add_tex_id( "t_"+mat_name, shinny, tex_file ,u,v,du,dv   )
       #tex_id=0


       mat= self.get_material_id( mat_name )
       
       tf,ti,mt= self.get_mat_pos()
       vi=mt[0]+mat*44
       btf,bti,bmt= self.get_mat_info()
       tex_id = bti.index( tex_id_name   )
       
       self.data[vi+16 ]  = orientation
       self.data[vi+36 ]  = tex_id  +0
       self.data[vi+40 ]  = tex_id  +0
       print  mat_name, "  -> ", tex_id_name
 
       
   def new_tex_id( self,tname  ):
       tf,ti,mt= self.get_mat_pos()
       for j in range(24):
           self.data.insert( ti[0] + 24*ti[1],  0 )
           
       for j in range(min(12,len(tname) )):self.data[  ti[0] + 24*ti[1]+j  ] =ord(tname[j])

       
       vi = ti[0]+0
       vi-=4
       self.data[vi ] +=1      
  

       self.update_geo_num()
       
       return  self.data[vi]-1

    
   def set_tex_id(self, tname ,sh ,  tex_file_id, u,v,du,dv , orie=0 ):
       #tf,ti,mt= self.get_mat_pos()
       tf,ti,mt= self.get_mat_info()
       if  tname in ti:
           tid = ti.index(tname)
       else:
           tid= self.new_tex_id(tname)
           
       tf,ti,mt= self.get_mat_pos()
       vi = ti[0] + tid * 24
       self.data[vi+16 ]= sh
       self.data[vi+17 ]=orie
       self.data[vi+18 ]=tex_file_id 
       
       self.data[vi+20 ]=du+0
       self.data[vi+21 ]=dv+0       
       self.data[vi+22 ]=u+0
       self.data[vi+23 ]=v+0
       
       return tid 
	   
   def glue_vertex(self, vtx, fc1, fc2, dist=0.01 ):
    self.update_geo_num()
    print "----------------------------\n\n"
    print vtx[0]
    v1=[]
    v2=[]
    vc={}
    for f1 in fc1:
      v1.extend(f1)
      
    for f2 in fc2:
      v2.extend(f2)
    dg=0
    for u1 in v1:
      dmin = dist +0 
      vc[u1+0]=u1+0
      for u2 in v2:
          
          if  abs( vtx[u1][0] - vtx[u2][0] ) > dmin: continue 
          if  abs( vtx[u1][1] - vtx[u2][1] ) > dmin : continue 
          if  abs( vtx[u1][2] - vtx[u2][2] ) > dmin : continue
          dmin = min( [ abs( vtx[u1][k] - vtx[u2][k] ) for k in (0,1,2)  ])
          vc[u1+0] = u2+0
          dg+=1
          
    for i in range(len(fc1)):
       fc1[i][0] = vc[ fc1[i][0] ]
       fc1[i][1] = vc[ fc1[i][1] ]
       fc1[i][2] = vc[ fc1[i][2] ]
    print "weld ",dg 
    self.update_geo_num()	
    return fc1
   
   def write(self,fname):
    f= open(fname,"wb")
    for x in self.data:
       f.write(struct.pack("B",x) )   
    f.close()   


##
##if __name__ == '__main__':
##    
##  fl =   "teste.jpg"
##  if os.path.exists(fl ):  os.remove(fl)
##  s= blk_file() 
##  s.load("c:\\tmp\\XR_original.vob")
##
##
##  for me in range(1,9):
##    s.set_mid(me)  
##    ti = s.dump_mesh_as_string()
##    open("XR_%i.obj"%(me),"w").write("".join(ti))
##    
##
##         
##  obj_id = s.get_obj_names().index("M1_side")
##
##  
##  mat_name= s.get_obj_material( "M1_side")         
##  mat= s.get_material_id( mat_name )
##  
##  tf,ti,mt= s.get_mat_pos()
##  vm= mt[0]+mat*44
##  
##  #print  ss(range(24))
##  j=17
##  s.data[vm+17 ] =15
##  #print  ss(s.data[vm:vm+24 ])
##  for i in range( ti[1]):
##    vm= ti[0]+i*24 
##    #print  ss(s.data[vm:vm+24 ])
##
##  oname= "M1_side"
##  mat_name = s.get_obj_material( oname )
##  s.set_tex_id( 'Left',  2, 0, 0,0,32,32,3 )
##  s.set_tex_id( 'Right',  2, 0, 0,0,32,32,3 )
##
##  #fit_area(x1,x2,y1,y2,du,dv, two_side=True, ratio =True )
##  
##  x1,x2,y1,y2=  s.get_axis_limits( "M1_side",[0,1,3],  3 )
##  print x1,x2,y1,y2
##  x1,x2,y1,y2,du,dv = fit_area(x1,x2,y1,y2,48,16, two_side=True, ratio =True )
##  
##  print abs(x2-x1)/abs(y2-y1), " du,dv=", du,float(dv)
##
##  s.set_tex_id( 'Left',  2, 0, 0,0,du,dv,2 )
##  s.set_tex_id( 'Right',  2, 0, 0,0,du,dv,2 )
##  
##  obj_ic= s.get_obj_names().index("M1_side")
##  s.render_template( obj_ic, 0 ,"teste.jpg" )
##  s.render_template( obj_ic, 1 ,"teste.jpg" )
##  s.render_template( obj_ic, 3 ,"teste.jpg" )
##
##
## 
##  #s.set_material(  mat_name , False , 3, tex_slots, texture_file )
##  
##  #obj_ic= s.get_obj_names().index("M2_Bonn")
##  
##  #s.render_template( obj_id, 4 ,"teste.jpg" )
##  #s.render_template( obj_ic, 0 ,"teste.jpg" )
##  #s.render_template( obj_ic, 1 ,"teste.jpg" )
##  #s.render_template( obj_ic, 4 ,"teste.jpg"  )  
##  #print s.nv, s.nf,s.get_obj_names()
##  #print s.get_mat_info()
##  s.write("D:\\Documents and Settings\\User\\Desktop\\LFS_S2_ALPHA_Z\\data\\veh\\XR.vob")
## 
##
##
###s= blk_file()
###s.load("c:\\tmp\\XR_original.vob")
###s.set_mid(1)
## 
##
##
###print s.get_mat_info()
##
## 
###s.set_material("TOP" , 1,0,[0], "LEXUS")
###print s.get_mat_info()
##
###print calc_slot( [2,3] )
###s.scan_normals(26,  q=0.2 )
###g= s.get_obj_names()
###print g
###fr=  s.get_obj_material( "M1_side" )
###print s.get_material_bb(  fr )
###for i in range(len(g)):    print i,g[i]
## 
