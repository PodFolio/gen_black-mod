

import struct
import math
import random

from  objread import *

uniqueNumberInternal = 0

mesh_id=1
vobname= "C:\\Documents and Settings\\Henrique.CATALDO-FE60ADE\\Desktop\\Conversor\\F01.vob"
vob_saida= "C:\Documents and Settings\\Henrique.CATALDO-FE60ADE\\Desktop\\gen_vob\\F1.vob"
text_file="C:\\Documents and Settings\\Henrique.CATALDO-FE60ADE\\Desktop\\Conversor\\cmd.txt"
obj_file="C:\\Documents and Settings\\Henrique.CATALDO-FE60ADE\\Desktop\\Conversor\\F109.obj"
def uniqueNumber():
    global uniqueNumberInternal
    uniqueNumberInternal += 1
    return uniqueNumberInternal

def unpackColor(x):
    return (ord(x[1])/255.0,ord(x[2])/255.0,ord(x[3])/255.0,(255-ord(x[0]))/255.0)


def f_unifica(seq):
    # Not order preserving
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()

    
def int2m(x):
    return x/65536.0

def fixed(sd):
    #print "FIX", sd
    s= chr( sd[0]) + chr(sd[1]) +chr( sd[2]) +chr( sd[3]) 
    return  (struct.unpack("i",s)[0])/65536.0

def readIntm(f):
    return int2m(readInt(f))

def readInt(f):
    sd=f.read(4)    
    return struct.unpack("i",sd)[0]

def readFloat(f):
    s = f.read(4)
    try:
        return struct.unpack("f",s)[0]
    except:
        print s
        raise sys.exception
def readbyte(f):
    return struct.unpack("B",f.read(1))[0]


def readUWord(f):
    return struct.unpack("H",f.read(2))[0]

def readWord(f):
    return struct.unpack("h",f.read(2))[0]

def unpackString(x):
    s = ''
    for c in x:
        if ord(c)==0:
            break
        s += c
    return s

import sys
import os



def get_near(vlist,x,y,z,ed=0.10):
    vout=None
    for i in range(len(vlist)):
        vk= vlist[i]
        if abs(vk[0] - x) > ed : continue
        if abs(vk[1] - y) > ed : continue  
        if abs(vk[2] - z) > ed : continue
        vout=i+0
        return vout
    return None 

def znormal(p1,p2,p3):
    d1=p3[0]-p1[0],p3[1]-p1[1],p3[2]-p1[2]
    d2=p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]
    x=d1[1]*d2[2]- d1[2]*d2[1]
    y=d1[0]*d2[2]- d1[2]*d2[0]
    z=d1[1]*d2[0]- d1[0]*d2[1]
    return x,y,z
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

def str_to_bin(s,size):
            d=[0 for i in range(size)]
            for j in range(min(size,len(s))): d[j]=ord(s[j])
            return d

def bin_v(x,y,z):
            s=  (struct. pack("iii",x*65536.0,y*65536.0,z*65536.0))
            return [ ord(i) for i in s]
        
def bin_vd(d,x,y,z):
            s=  (struct. pack("iii",x*65536.0,y*65536.0,z*65536.0))
            return [d,0,0,0]+[ ord(i) for i in s]

        
def to_word(x):
            if x > 65530: print "OVERFLOW \n\n\n" 
            return x&0xff, (x&0xff00)/256
#classes basicas

class OBJETO:
    #objeto contem um conjunto de vertices do mesmo material
    def __init__(self,name):
        self.name=name
        self.iname=[]
        self.color=(0.5,0.5,0.5)
        self.material=None
        self.mat_id=0
        self.math_id_num=0
        self.vt=[] #vertice 
        self.tx=[] #textura de cada ponto
        self.fc=[] #lista das faces
        self.fflags=[]
        self.vflags=[]
        self.nv=[] #normais de cada face
        self.glist=None
        self.tipo=0
        self.type_render=1
        self.id=0
        self.enable=True
        self.GLcalllist=None

        
    def add_face(self,xyz1,xyz2,xyz3, fbin=None, vbin=None ):
 
        #insere 3 pontos
        ni=len(self.vt)
        self.vt.append(xyz1)
        self.vt.append(xyz2)
        self.vt.append(xyz3)
        if vbin==None:
          self.vflags.append([0,0,0,0])
          self.vflags.append([0,0,0,0])
          self.vflags.append([0,0,0,0])
        else:
          self.vflags.append(vbin[0])
          self.vflags.append(vbin[1])
          self.vflags.append(vbin[2])  
        if fbin!=None:
           self.fflags.append(fbin)
           #fbin[0] | 16 = 16 : nao facao mirror desta face  
        else:
           self.fbin=[0,0,0,0,0,0,0,0,0,0,0,0]

        self.fc.append([ni,ni+1,ni+2])
        self.nv.append(znormal( xyz1,xyz2,xyz3  ) )


    def add_data(self,list_obj,list_vtx,list_fcs,list_mat):
        
        oid=len(list_obj)        
        data_o=[0,0,0,0]
        data_o[0]=int(self.color[0]*255)&0xff
        data_o[1]=int(self.color[1]*255)&0xff
        data_o[2]=int(self.color[2]*255)&0xff
        data_o[3]=int(self.color[3]*255)&0xff
        
        mt_num=0 #default
        for i in range(len(list_mat)):
            if  list_mat[i][0] == self.mat_id:
               mt_num=i+0
               break
        #data_o=data_o+str_to_bin(  self.material,10 )+[ mt_num ]+[0]
        
        list_obj.append([ self.material , data_o+[] , mt_num+0 ])
        
        #print "@",list_obj[-1]
        #list_obj.append(data_o+[])
        

    
        #adiciona os vertices
        vi=len(list_vtx)
        for k in range(len(self.vt)):
          v1= self.vt[k]

          list_vtx.append( self.vflags[k] +bin_v(*v1))
          
        for i in range(len(self.fc))  :            
            fbin= [0,0,0, 0,0,0, 0,0,0, 0,0,0]
            v1,v2,v3= self.fc[i][0],self.fc[i][1],self.fc[i][2]            
            fbin[6],fbin[7]= to_word(v1+vi)
            fbin[7]=fbin[7]|(  self.fflags[i][7]&0xf000   )
            fbin[8],fbin[9]= to_word(v2+vi)
            fbin[9]=fbin[9]|(  self.fflags[i][9]&0xf000   )
            fbin[10],fbin[11]= to_word(v3+vi)
            fbin[11]=fbin[11]|(  self.fflags[i][11]&0xf000   )
            fbin[2]=oid+0
            
            fbin[0]=self.fflags[i][0]
            fbin[1]=self.fflags[i][1]
            #fbin[2]=self.fflags[i][2]            
            fbin[3]=self.fflags[i][3]
            fbin[4]=self.fflags[i][4]
            #fbin[5]=self.fflags[i][5] #controla as normais ?
            list_fcs.append(fbin)
            
        return list_obj,list_vtx,list_fcs,list_mat
    
    def geo_render(self):
         for f in range( len(self.fc) ):
           if   self.fflags[f][4]>0:
               continue
           glNormal3fv(self.nv[f] )       
           for vi in self.fc[f]:       
              glVertex3fv( self.vt[ vi ]  )

           if self.fflags[f][0]   & 16 == 0:
             glNormal3fv(self.nv[f] )       
             for vi in self.fc[f]:       
                glVertex3f( -self.vt[ vi ][0],self.vt[ vi ][1], self.vt[ vi ][2]    )               
         #glEnd()
              
    def render(self ):
           #self.geo_render()
           #return
           if self.enable==False:
               return
           if len(self.fc)==0: return
           
           glColor3fv(self.color[0:3])
           glMaterialfv(GL_FRONT,GL_DIFFUSE,self.color)
           #glDisable(GL_LIGHTING)
           #glEnable(GL_CULL_FACE)         

              
           if (self.GLcalllist is None):
                self.GLcalllist = glGenLists(1)
                glNewList(self.GLcalllist, GL_COMPILE)                
                self.geo_render()
                glEndList()

           
           
   

           if self.type_render==1:
              glBegin(GL_TRIANGLES)
           else:
              glBegin(GL_TRIANGLES)
              #glBegin(GL_LINE_STRIP)
           #self.geo_render()              
           glCallList(self.GLcalllist) 
           glEnd()

           




# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0


 
vv=[]
ff=[] #v1,v2,v3, R,G,B

rtri =0.0

def ss(g,x=3):
    s=""
    for i in g:
        if x==3:
          s+="%03i "%(i)
        if x==5:s+="%5i "%(i)
    return s




    
def read_axyz(d):
                   vi=0
                   s=fixed(d[vi:vi+4 ]);vi+=4
                   x=fixed(d[vi:vi+4 ]);vi+=4
                   y=fixed(d[vi:vi+4 ]);vi+=4
                   z=fixed(d[vi:vi+4 ]);vi+=4
                   return [s,x,y,z]

def find_header(data,voff):
    i=voff -1
    # suponha que este o numero de vertices esta em vs+30
    start=False
    while start==False:
        start=True
        i+=1
        if i > len(data):
             print "end of file ",i 
             return None,None
            
        nv=data[i] + data[i+1]*256
        nf=data[i+2] + data[i+3]*256           
        mn=data[i+30]  # offset 60

        if  mn<1  or nv <3 or nf < 9:
            #print "null ojs ",i
            start=False
            continue 
            
        off_obj= i+32  # offset 62
        
        #testa os objetos, cada objeto deve ter a primeira letra valida
        #print "--------------------------"
        for k in range(mn):
            for l in range(3):
              name= data[off_obj +4 + 16*k  + l  ]
              if  name>150 : # or name < 10:
                  start=False
                  break                
            #if start==True :
            #   print toname( data[off_obj+4 + 16*k :  off_obj+4 + 16*(k+1) ] )
            
        if start==False: continue

        #print "OK.. pass ", i
        
        off_vi=  off_obj + 16*mn
        off_fc=  off_vi + 16* nv
        face_end= off_fc + nf*12

        #testa os vertices
        
        for k in range(nv):
            kv= k*16 + off_vi
            a,x,y,z= read_axyz(data[kv :kv +16])
            if data[kv+1]>0 or  data[kv+2]>0 or data[kv+3]>0 :
               #print "vertex err " 
               start=False
               break
            
            if abs(x)> 6 or abs(y) > 6:
               start=False
               break
            
            
        if start==False: continue
        #print "vertex pass at ",i
        tex_off=face_end+0
        while data[tex_off]==0:  tex_off +=1
        
        num_tex=data[tex_off]
        tex_off+=4
        vi= tex_off +0
        for j in range(num_tex):
            skp_name=data[ tex_off + 20 * j +4 ]
            if skp_name <20 or skp_name>150:
                  #start=False
                  break
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
        #print "-----"*4    
        #print "found ", i
        #print "  NVERTEX ",nv
        #print "  NFACES ",nf
        #print "  NOBJS ",mn
        #print " next ", vi
        return i,vi
    
    
def move_vertex(data,vi,dx,dy,dz):
    #adiciona um vertice e devolve o indice dele e os dados
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv
    
    #for j in range(nf):
    #     lz=12
    #     print ss(data[ lz*j+off_fc:lz*(j+1)+off_fc   ])
    #if abs(x) < 0.01: x=0.0 
    s,x,y,z= read_axyz( data[off_vi+ 16* vi : off_vi+ 16* (vi+1) ]  )
    
    vdata= bin_vd(1,x+dx,y+dy,z+dz)
    for j in range(4,16):
      data[ j+off_vi+ 16* vi ] =   vdata[j]

      
    #data[i],data[i+1] = to_word(nv+1)    
    #for j in range(16):    
    #data.insert(j+off_fc, vdata[j] )
    return   data


def remove_pts(data,obj_name, vs ):
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    

    obj_idx=None
    for j in range(mn):
        oz= data[off_obj+j*16:off_obj+j*16+16 ]
        #print oz
        RGBA=oz[0:4]
        RGBA=[g/256.0 for g in oz[0:4]]
        name= toname(oz[4:14])
        name.replace(" ","_")
        
        #print name 
        if name==obj_name:
            obj_idx= j+0
            break
    if obj_idx==None:
       #print "obj ", obj_name," not found"
       #print "procurando mais provavel"
       for j in range(mn):
            oz= data[off_obj+j*16:off_obj+j*16+16 ]
            #print oz
            RGBA=oz[0:4]
            RGBA=[g/256.0 for g in oz[0:4]]
            name= toname(oz[4:14])
            #print name
            
            if name==obj_name[0:len(name)]:
                obj_idx= j+0
                #print "mais provavel ",obj_name 
                break
            
       
       return data
    #remove de forma seletiva
    nfk=nf+0
    j=0
    #print "Clean obj num", obj_idx
    cnf=0
    while j < nfk:    
        fi= off_fc + j*12
        if data[fi+2]==obj_idx and data[fi+3]!=99 and    data[fi+4]==0 :
           #delete
           #k1= data[fi+6] + 256* data[fi+7]
           #k2= data[fi+8] +  256* data[fi+9]
           #k3= data[fi+10] + 256*  data[fi+11]
           #if  k1 < nf and k2 < nf and k3 < nf :
           if True:    
             #for h in range(12): 
                 #del data[fi]
                 v3,v2,v1 = data[fi+10]+256*(data[fi+11]),data[fi+8]+256*(data[fi+9] ), data[fi+6]+256*(data[fi+7])
                 cnf+=1
                 clipp=False
                 for j in (v1,v2,v3):
                     s,x,y,z= read_axyz( data[off_vi+ 16* j : off_vi+ 16* (j+1) ])
                     for kk in vs:
                       if abs (x-kk[0]) < 0.004 and  abs(y-kk[1]) < 0.004 and  abs(z-kk[2]) < 0.004:
                        clipp=True
                        break
                 if clipp :
                   nfk=nfk-1  
                   for h in range(12): 
                       del data[fi]
                 else:
                    j+=1      
               
        else:
           j+=1 
    data[i+2],data[i+3] = to_word( nfk)
    print "clean ", cnf, " vtx"
    #print
    return data




    

def clip_vertex_if(data, obj_name, cmd ,model=0 ):

    x00= bin_vd(0,0,0,0)
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    

    obj_idx=None
    for j in range(mn):
        oz= data[off_obj+j*16:off_obj+j*16+16 ]
        #print oz
        RGBA=oz[0:4]
        RGBA=[g/256.0 for g in oz[0:4]]
        name= toname(oz[4:14])
        #print name 
        if name==obj_name:
            obj_idx= j+0
            break
    if obj_idx==None:
       #print "obj ", obj_name," not found"
       #print "procurando mais provavel"
       for j in range(mn):
            oz= data[off_obj+j*16:off_obj+j*16+16 ]
            #print oz
            RGBA=oz[0:4]
            RGBA=[g/256.0 for g in oz[0:4]]
            name= toname(oz[4:14])
            #print name
            
            if name==obj_name[0:len(name)]:
                obj_idx= j+0
                #print "mais provavel ",obj_name 
                break
            
       
       return data
    #remove de forma seletiva
    nfk=nf+0
    j=0
    #print "Clean obj num", obj_idx
    cnf=0
    while j < nfk:
        j+=1
        fi= off_fc + j*12
        if data[fi+2]==obj_idx and data[fi+3]!=99 and    data[fi+4]==0 :
           #delete
           #k1= data[fi+6] + 256* data[fi+7]
           #k2= data[fi+8] +  256* data[fi+9]
           #k3= data[fi+10] + 256*  data[fi+11]
           #if  k1 < nf and k2 < nf and k3 < nf :
           if True:    
             #for h in range(12): 
                 #del data[fi]
                 v3,v2,v1 = data[fi+10]+256*(data[fi+11] & 0x127 ),data[fi+8]+256*(data[fi+9] & 0x127  ), data[fi+6]+256*(data[fi+7] & 0x127 )
                 #cnf+=1
                 clipp=False
                 for jj in (v1,v2,v3):
                      
                     s,x,y,z= read_axyz( data[off_vi+ 16* jj : off_vi+ 16* (jj+1) ])
                     sn= cmd(x,y,z,s)
                     if sn!=False:
                        cnf+=1
                        clipp=True
                        #break
                        # if clipp ==True:
                        x00=   bin_vd(0,sn[0],sn[1],sn[2])
                        print x,y,z ," -> ", sn[0],sn[1],sn[2]
                        for h in range(4,16):  data[off_vi+ 16* jj +h   ]= x00[h]
                   
 
                 
                 else:
                    #j+=1
                    pass
               
        else:
           #j+=1
           pass
        
    #data[i+2],data[i+3] = to_word( nfk)
    print "clean ", cnf, " vtx"
    #print
    return data
    

def clip_vertex(data, dx,dy,dz):
    #adiciona um vertice e devolve o indice dele e os dados
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv
    
    for vi in range(nv):
       s,x,y,z= read_axyz( data[off_vi+ 16* vi : off_vi+ 16* (vi+1) ])
       if x >= dx :
          x=0.0
          vdata= bin_vd(1,0,y,z)
          for j in range(0,16):
             data[ j+off_vi+ 16* vi ] =   vdata[j]
    return   data 
 

def scale_vertex(data, dx,dy,dz):
    #adiciona um vertice e devolve o indice dele e os dados
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv
    
    for vi in range(nv):
       s,x,y,z= read_axyz( data[off_vi+ 16* vi : off_vi+ 16* (vi+1) ])
       
           
       vdata= bin_vd(1,x*dx,y*dy,z*dz)
       for j in range(4,16):
             data[ j+off_vi+ 16* vi ] =   vdata[j]
    return data



def vob_raw_obj(data, obj_name,mat=0, cor=(255,255,255)  ):
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]    
    off_obj= 72-14+4
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv

    oz= [0 for j in range(16) ]
        #print oz
    
    oz[0],oz[1],oz[2]=cor[0],cor[1],cor[2]
    oz[3]=0
    
    #    RGBA=[g/256.0 for g in oz[0:4]]
    for k in range( min(8, len(obj_name))):
        oz[4+k]= ord(obj_name[k])
        oz[14],oz[15]=  to_word( mat)                    

    for j in range(16):
        data.insert(  j+off_vi, oz[j] )                
    data[72-14+2] = mn+1
                    
    return data


def vob_vertex_list(data):
    
    #adiciona um vertice e devolve o indice dele e os dados
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv
    
    #for j in range(nf):
    #     lz=12
    #     print ss(data[ lz*j+off_fc:lz*(j+1)+off_fc   ])

 
    pv=[]
    for vi in range(nv):        
      s,px,py,pz= read_axyz( data[off_vi+ 16* vi : off_vi+ 16* (vi+1) ])
      pv.append([px+0,py+0,pz+0])
    return pv


def vob_add_vertex(data,x,y,z,mirror=True):


    
    #adiciona um vertice e devolve o indice dele e os dados
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv
    
    #for j in range(nf):
    #     lz=12
    #     print ss(data[ lz*j+off_fc:lz*(j+1)+off_fc   ])

 
    insert =True    
    if insert ==True:
        if abs(x) < 0.01:
            x=0.0 
            vdata= bin_vd(2,x,y,z)
        else:
            vdata= bin_vd(1,x,y,z)

            
       # if mirror=="FX":       vdata[0]=0
            
        data[i],data[i+1] = to_word(nv+1)
        #for j in range(16):  data.insert(j+off_fc , vdata[j] )
        data[ off_fc :  off_fc] = vdata
    return nv, data


def vob_remove_faces( data,obj_name , model=0 , wig=0):
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    

    obj_idx=None
    for j in range(mn):
        oz= data[off_obj+j*16:off_obj+j*16+16 ]
        #print oz
        RGBA=oz[0:4]
        RGBA=[g/256.0 for g in oz[0:4]]
        name= toname(oz[4:14])
        #print name 
        if name==obj_name:
            obj_idx= j+0
            break
    if obj_idx==None:
       #print "obj ", obj_name," not found"
       #print "procurando mais provavel"
       for j in range(mn):
            oz= data[off_obj+j*16:off_obj+j*16+16 ]
            #print oz
            RGBA=oz[0:4]
            RGBA=[g/256.0 for g in oz[0:4]]
            name= toname(oz[4:14])
            #print name
            
            if name==obj_name[0:len(name)]:
                obj_idx= j+0
                #print "mais provavel ",obj_name 
                break
            
       
       return data
    #remove de forma seletiva
    nfk=nf+0
    j=0
    #print "Clean obj num", obj_idx
    cnf=0
    while j < nfk:    
        fi= off_fc + j*12
        if data[fi+2]==obj_idx and data[fi+3]!=99 and    data[fi+4]==0 :
           #delete
           #k1= data[fi+6] + 256* data[fi+7]
           #k2= data[fi+8] +  256* data[fi+9]
           #k3= data[fi+10] + 256*  data[fi+11]
           #if  k1 < nf and k2 < nf and k3 < nf :
           if True:    
             for h in range(12): 
                 del data[fi]
             cnf+=1
             nfk-=1
           else:
              j+=1 
        else:
           j+=1 
    data[i+2],data[i+3] = to_word( nfk)
    print "clean ", cnf, " faces"
    #print
    return data


def vob_remove_mesh( data, ni , wig=0):    
    i=0
    v1=0
    v2=0
    n=ni+0
    while n >0 :
      n=n-1  
      v1,v2 =  find_header(data,v2)
           
    i=v1
    
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[i+30]
    
    off_obj= i+32
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    

    obj_idx=None
##    for j in range(mn):
##        oz= data[off_obj+j*16:off_obj+j*16+16 ]
##        #print oz
##        RGBA=oz[0:4]
##        RGBA=[g/256.0 for g in oz[0:4]]
##        name= toname(oz[4:14])
##        #print name 
##        if name==obj_name:
##            obj_idx= j+0
##            break
##    if obj_idx==None:
##       print "obj ", obj_name," not found"
##       print "procurando mais provavel"
##       for j in range(mn):
##            oz= data[off_obj+j*16:off_obj+j*16+16 ]
##            #print oz
##            RGBA=oz[0:4]
##            RGBA=[g/256.0 for g in oz[0:4]]
##            name= toname(oz[4:14])
##            #print name
##            
##            if name==obj_name[0:len(name)]:
##                obj_idx= j+0
##                print "mais provavel ",obj_name 
##                break
            
       
    #   return data
    #remove de forma seletiva
    nfk=nf+0
    j=0
    #print "Clean obj num", obj_idx
    cnf=0
    while j < nfk:    
        fi= off_fc + j*12
        if  data[fi+3]!=99 and    data[fi+4]==0 :
           #delete
           #k1= data[fi+6] + 256* data[fi+7]
           #k2= data[fi+8] +  256* data[fi+9]
           #k3= data[fi+10] + 256*  data[fi+11]
           #if  k1 < nf and k2 < nf and k3 < nf :
           if True:    
             for h in range(12): 
                 del data[fi]
                 pass
             cnf+=1
             nfk-=1
           else:
              j+=1 
        else:
           j+=1 
    data[i+2],data[i+3] = to_word( nfk)
    print "clean ", cnf, " faces"
    #print
    return data





def vob_remove_faces_ex( data,obj_name , model=0 , wig=0):
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    

    obj_idx=None
    for j in range(mn):
        oz= data[off_obj+j*16:off_obj+j*16+16 ]
        #print oz
        RGBA=oz[0:4]
        RGBA=[g/256.0 for g in oz[0:4]]
        name= toname(oz[4:14])
        #print name 
        if name==obj_name:
            obj_idx= j+0
            break
    if obj_idx==None:
       #print "obj ", obj_name," not found"
       #print "procurando mais provavel"
       for j in range(mn):
            oz= data[off_obj+j*16:off_obj+j*16+16 ]
            #print oz
            RGBA=oz[0:4]
            RGBA=[g/256.0 for g in oz[0:4]]
            name= toname(oz[4:14])
            #print name
            
            if name==obj_name[0:len(name)]:
                obj_idx= j+0
                #print "mais provavel ",obj_name 
                break
            
       
       return data
    #remove de forma seletiva
    nfk=nf+0
    j=0
    #print "Clean obj num", obj_idx
    cnf=0
    while j < nfk:    
        fi= off_fc + j*12
        if data[fi+2]==obj_idx and data[fi+3]!=99 and    data[fi+4]==0 and data[fi+4]==model :
           #delete
           #k1= data[fi+6] + 256* data[fi+7]
           #k2= data[fi+8] +  256* data[fi+9]
           #k3= data[fi+10] + 256*  data[fi+11]
           #if  k1 < nf and k2 < nf and k3 < nf :
           if True:    
             for h in range(12): 
                 del data[fi]
             cnf+=1
             nfk-=1
           else:
              j+=1 
        else:
           j+=1 
    data[i+2],data[i+3] = to_word( nfk)
    #print "clean ", cnf, " faces"
    #print
    return data    


def vob_clean_all(data,i1,i2):
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    


    nfk=nf+0
    j=0
    while j < nfk:    
        fi= off_fc + j*12
        #if data[fi+4]!=0:
           # print ss(data[fi:fi+12])
        if data[fi+4]==0  and data[fi+2]>=i1  and  data[fi+2]<= i2 :
           if True:
             for h in range(12): 
                 del data[fi]
             nfk-=1
           else:
              j+=1 
        else:
           j+=1 
    data[i+2],data[i+3] = to_word( nfk)
    return data


def vob_remove_faces_id( data,obj_id , model=0 , wig=0):
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    

    obj_idx=obj_id
##    for j in range(mn):
##        oz= data[off_obj+j*16:off_obj+j*16+16 ]
##        #print oz
##        RGBA=oz[0:4]
##        RGBA=[g/256.0 for g in oz[0:4]]
##        name= toname(oz[4:14])
##        #print name 
##        if name==obj_name:
##            obj_idx= j+0
##            break
        
    if obj_idx==None:
       print "obj ", obj_name," not found"
       return data
    #remove de forma seletiva
    nfk=nf+0
    j=0
    while j < nfk:    
        fi= off_fc + j*12
        #if data[fi+2]==obj_idx:
        #   print [  " %03i"%(kk)  for kk in  data[fi : fi+6]   ]
        if data[fi+2]==obj_idx   and   data[fi+4]==0 :
           #delete
           #k1= data[fi+6] + 256* data[fi+7]
           #k2= data[fi+8] +  256* data[fi+9]
           #k3= data[fi+10] + 256*  data[fi+11]
           #if k1 < nf and k2 < nf and k3 < nf :
           if True:
             for h in range(12): 
                 del data[fi]
             nfk-=1
           else:
              j+=1 
        else:
           j+=1 
    data[i+2],data[i+3] = to_word( nfk)
    return data


def get_material_pos(data):
    #devolve tex_file(offset,num), tex_id(offset,num),material(offset_num)
    out=[]
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv

    face_end= off_fc + nf*12
    
    tex_off=face_end+0

    
    #print "TEX ", tex_off

    
    while data[tex_off]==0:  tex_off +=1
    num_tex=data[tex_off]
    tex_off+=4
    vi= tex_off +0
    out.append([tex_off +0, num_tex+0 ] )    
    for i in range(num_tex):
        #tex_data=data[vi:vi+4]
        #tex_nome=data[vi+4:vi+20]
        #print "%3i"%(i), toname(tex_nome), tex_data
        #textures_files.append(toname(skp_nome)) #==============
        vi+=20
        
    ktex_num= data[vi] +256*  data[vi+1]

    #print "ID ", ktex_num
    vi+=4
    tex_id_off = vi+0
    out.append([vi +0, ktex_num+0 ] )    
    for i in range(ktex_num):
       #ktex_name= data[vi:vi+16]       
       #ktex_data= data[vi+16:vi+24]
       #print data[vi:vi+24]
       #data[vi+16:vi+22]= [0,0,0,0,0,0 ]
       #data[vi+16+6] = 12
       #data[vi+16+7] = 12       
       #print"%3i"%(i), toname(ktex_name,True) ,  ss(ktex_data)
       #tex_if.append( [toname(ktex_name),ktex_data+[],textures_files[ktex_data[2]][0] ]  )#=========
       vi+=24
    num_mat=data[vi]+0
    vi+=4
    out.append([vi +0, num_mat+0 ] )
    
    for j in range(num_mat):
            mat_name=data[vi:vi+15]
            #print "%3i"%(j),toname( mat_name )
            vi+=44
    #print out        
    return out


def get_texture_file_byname(data,qname):
    tf,ti,mt= get_material_pos(data )
    vi, num_tex= tf[0], tf[1]
    for i in range(num_tex):
        #tex_data=data[vi:vi+4]
        tex_nome=toname(data[vi+4:vi+20])
        if tex_nome == qname: return i
        #print "%3i"%(i), toname(tex_nome), tex_data
        #textures_files.append(toname(skp_nome)) #==============
        vi+=20
    print "ERROR: TEXTURE FILE NOT FOUND" , qname   
    #raise NameError   
    return None    


def get_texture_id_byname(data,qname):
    tf,ti,mt= get_material_pos(data )
    vi, num_tex= ti[0], ti[1]
    for i in range(num_tex):
        #tex_data=data[vi:vi+4]
        tex_nome=toname(data[vi:vi+16] )
        if tex_nome == qname:
            print "Texture name found ", toname(data[vi:vi+16] )
            return i
        #print "%3i"%(i), toname(tex_nome), tex_data
        #textures_files.append(toname(skp_nome)) #==============
        vi+=24
    print "ERROR: TEXTURE ID NOT FOUND"  ,qname  
    #raise NameError   
    return None



def new_tex_file(data,fname):
    tf,ti,mt= get_material_pos(data )    
    data[tf[0]-4 ],data[tf[0]-3 ] = to_word( tf[1]+1  )    
    fp = [0 for i in range(20) ]
    for i in range(min(len(fname), 15) ): 
      fp[i+4] =ord(fname[i])
    for k in range(20):  
      data.insert( tf[0] +  tf[1]* 20 +k, fp[k])
    print "new texture ADD: ",fname  
    return data  



    
def new_tex_id(data,name, param=[] ):
    tf,ti,mt= get_material_pos(data )    
    data[ti[0]-4 ],data[ti[0]-3 ] = to_word( ti[1]+1)
    for k in range(24):
        if k < min(15,len(name)):
           data.insert( ti[0]+ ti[1]* 24 + k, ord(name[k])  )            
        else:
           data.insert( ti[0]+ ti[1]* 24 + k,0 )    
    return data


def set_tex_param_material(data,mat_name, tfile ,  param ):
    tf,ti,mt= get_material_pos(data )    
    vi = mt[0]+0
    cp=[]
    tex_1=None
    tex_2=None 
    #print "NUM ",mt[1] 
    for i in range(mt[1]):
        #print toname(data[vi:vi+15]), mat_name
        if toname(data[vi:vi+15])==mat_name:            
           tex_1= data[vi+36]
           tex_2= data[vi+41]
        vi+=44
    if tex_1==None:
       print "NOT FOUNT MATERIAL ",mat_name
       raise NameError
    data = set_tex_param_id(data, tex_1 , tfile ,  param)
    data = set_tex_param_id(data, tex_2 , tfile ,  param)
    return data

def set_tex_param_id(data, tid , tfile ,  param):    
    #tid = get_texture_id_byname(data, tex_name)
    if tid==None:
       raise NameError 
       #data= new_tex_file(data,tfile)
       #tid=-1

    tf_id= get_texture_file_byname(data,tfile)
    if tf_id==None:
      data= new_tex_file(data,tfile)
      tf_id= get_texture_file_byname(data,tfile)
    if tf_id==None:
       print "ERROR CRITICO, FILE TEXTURA NOT ADD ?" 
       raise NameError
       
    tf,ti,mt= get_material_pos(data )
    if tid >= ti[1]:
        print "ERROR on TEX PARAM"
        print type(ts )
        print "TEX ID =", ts , ti, ti[1]
        return data
    if tid < 0:
       tid= ti[1]+ tid  
       print "reset as ", tid
    #lets check the param
    param[2]= tf_id +0
    if param[2]<0:
       param[2]= tf_id[1] - param[2]
    print "-----------------------------------------------" 
    print "old param ",data[ ti[0]+tid*24  +16 :ti[0]+tid*24 + 8 +16 ]   
    print "new param", param   
    for i in range(min(len(param),8)):
        
        data[ ti[0]+tid*24 + i +16 ] = param[i]+0

    print "set ? param ",data[ ti[0]+tid*24  +16 :ti[0]+tid*24 + 8 +16 ]          
    return data






def set_tex_param(data, tex_name , tfile ,  param):    
    tid = get_texture_id_byname(data, tex_name)
    if tid==None:
       #data = new_tex_id(data,tex_name,[0,0,0,0,0,0,0,0,0] )

       raise NameError 
       #data= new_tex_file(data,tfile)
       #tid=-1

    tf_id= get_texture_file_byname(data,tfile)
    if tf_id==None:
      data= new_tex_file(data,tfile)
      tf_id= get_texture_file_byname(data,tfile)
    if tf_id==None:
       print "ERROR CRITICO, FILE TEXTURA NOT ADD ?" 
       raise NameError
       
    tf,ti,mt= get_material_pos(data )
    if tid >= ti[1]:
        print "ERROR on TEX PARAM"
        print type(ts )
        print "TEX ID =", ts , ti, ti[1]
        return data
    if tid < 0:
       tid= ti[1]+ tid  
       print "reset as ", tid
    #lets check the param
    param[2]= tf_id +0
    if param[2]<0:
       param[2]= tf_id[1] - param[2]
       
    for i in range(min(len(param),8)):
        data[ ti[0]+tid*24 + i +16 ] = param[i]+0

    print param
    print data[ ti[0]+tid*24  +16  :ti[0]+tid*24  +16 + 8   ]
    return data    


def set_tex_align_new(data,objname,   tfile , tsize, orient,vt1,vt2 ):
    def bin_nt(x,y,z,w ):
            s= (struct.pack("iiii",x*65536.0,  y*65536.0,z*65536.0,w*65536.0 ))
            return [ ord(i) for i in s]

    data= new_tex_id(data, "R"+objname ,[0,0,0,0,0,0,0,0,0,0,0,0])     
    data= set_tex_param(data, "R"+objname  , tfile , [ 0,0,0,0,64,64,0,0]  )
    
    return data


def set_material_param( data, mat_name ,  xyzw,  tx1, tx2):

    def bin_nt(x,y,z,w ):
            s= (struct.pack("iiii",x*65536.0,  y*65536.0,z*65536.0,w*65536.0 ))
            return [ ord(i) for i in s]

        
    mnew= get_material_id(data, mat_name  )

    tf,ti,mt= get_material_pos(data)
    vi= mt[0]+ mnew*44


    tmp =  bin_nt(*xyzw)
    for k in range(16):
        data[vi+20+k] = tmp[k]+0
    #data[vi+36]=tx1
    #data[vi+40]=tx2
    if tx1< 10:    
       data[vi+16]=tx1
       #data[17]=tx2
       #data[19]=0
    return data
        
    

        
def set_tex_align(data,objname,   tfile , tsize, flag, orient,vt1,vt2 ):  

    def bin_nt(x,y,z,w ):
            s= (struct.pack("iiii",x*65536.0,  y*65536.0,z*65536.0,w*65536.0 ))
            return [ ord(i) for i in s]
        
    #acha o objeto na tabela
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv

 
    mat=None

    obj_idd=0
    for i in range(mn):
        oz= data[off_obj+i*16:off_obj+i*16+16 ]
        #print oz
        #RGBA=oz[0:4]
        #RGBA=[g/256.0 for g in oz[0:4]]
        name= oz[4:14]+[]
        mat=oz[14]+256*oz[15]
        if toname(name)==   objname :
            mat=oz[14]+256*oz[15]
            obj_idd=i+0
            break
            
    if mat==None:
       print "ERROR, OBJ NOT FOUND"  
       return data



    #gera um novo material
    mat_name="m_"+objname

    #mnew=mat
    
    mnew= get_material_id(data, mat_name  )
    if mnew==None:   
        #acha o antigo material 
        tf,ti,mt= get_material_pos(data)
        vi= mt[0]+ mat*44
        old_mat_name = toname( data[vi: vi+15 ])        
        data = copy_material( data, old_mat_name , mat_name  )   
        #pega a nova id
        mnew= get_material_id(data, mat_name  )    
        #seta o novo material


    data[off_obj+obj_idd*16 +14], data[off_obj+obj_idd*16 +15]= to_word( mnew )



    data= new_tex_id(data, "t_"+objname  ,[0,0,0,0,0,0,0,0,0] )
    tid = get_texture_id_byname(data, "t_"+objname   )

    
    tf,ti,mt= get_material_pos(data)
    
    vi= mt[0]+  mnew *44

    data[vi+36 ]  = tid +0
    data[vi+40 ]  = tid+0
    
    return data

    #calcula os paraemtros de textura



    #cria um novo parametro de textura     
    tf,ti,mt= get_material_pos(data)
    #vi= mt[0]+ mnew*44    

    #tex_1=  data[vi+36]
    #tex_2=  data[vi+41]


    #computa obj size
    x1,y1,z1,u1,v1= vt1
    x2,y2,z2,u2,v2= vt2    
    du = int(abs(u2-u1)*64.0/1024.0 )
    dv = int(abs(v2-v1)*64.0/1024.0 )                
    u0 = int(min(u1,u2)*64.0/1024.0 )
    v0 = int(min(v1,v2)*64.0/1024.0 )                

     

    param=[0,0,0,0, 0,0,0,0  ]

    #param
    #0: ??
    #1: orientacao
    #2: texfile id
    #3  zero ?
    #4  delta u
    #5  delta v
    #6  desloc u
    #7  desloc v
 
                
    #tmp_data=[]

    tmp=[]
    if orient==1 or orient==0 or True:
       tmp =  bin_nt(x1,z1,x2,z2)
       #for j in range(16):         
       #    data[ vi + 5+j]=tmp[j]+0

           
    param[0]= flag  
    param[1]= orient
    param[4]= du+0
    param[5]= dv+0
    param[6]= u0+0
    param[7]= v0+0
    print  "PARAM TEX=",param
    tex_id_name ="cust_%i"%(obj_idd)


    #parametros calculados, busca por esta textura    
    tid = get_texture_id_byname(data, tex_id_name   )
    if tid ==None:
        print "GENERATE NEW TEX ID ",tex_id_name        
        data= new_tex_id(data,tex_id_name ,[0,0,0,0,0,0,0,0,0] )
        tid = get_texture_id_byname(data, tex_id_name)
    #ok, materia e textura ID novos
        
        
    tf,ti,mt= get_material_pos(data)
    vi= mt[0]+ mnew*44    
    data[vi+36] = tid+0
    data[vi+40] = tid+0
    
    #tex_2=  data[vi+41]
    for j in range(16):         
      data[ vi + 20+j]=tmp[j]+0
    
        
    data = set_tex_param(data, tex_id_name   , tfile ,  param)
    
    #data = set_tex_param_id(data, tex_2 , tfile ,  param) 
    return data


def get_material_id(data, mat_name):
    tf,ti,mt= get_material_pos(data )
    vi = mt[0]+0
    cp=[]
    for i in range(mt[1]):
        if toname(data[vi:vi+15])==mat_name:
           #pass 
           cp=data[vi:vi+44]+[]
           return i+0
        vi+=44
    return None
    

def copy_material( data, mat_name , new_name ):
    
    #copia o material de um dado objeto e coloca no final da lista de materiais    
    tf,ti,mt= get_material_pos(data )
    data[mt[0]-4], data[mt[0]-3] = to_word( mt[1]+1  )
    #print "  "
    vi = mt[0]+0
    cp=[]
    for i in range(mt[1]):
        if toname(data[vi:vi+15])==mat_name:
           #pass 
           cp=data[vi:vi+44]+[]        
        vi+=44
    #print ss( cp )    
    for k in range(44):
        data.insert(vi+k, cp[k])  #insere os novos dados
    #    pass
    for k in range(15):data[vi+k]=0   #limpa o nome antigo    
    for k in range(min(len(new_name),14)):  data[vi+k]= ord(new_name[k])  #seta novo nome
    #print ss( data[vi:vi+44])
    print "add material ",mat_name, " as " ,toname(data[vi:vi+44])
    #data[mt[0]-4], data[mt[0]-3] = to_word( mt[1]+1  )
    #get_material_pos(data )
    #print "END"
    return data




    
    

def new_material(data,name, param= [3, 0, 0, 0, 10]  ):
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv


   
    face_end= off_fc + nf*12
    tex_off=face_end+0
    while data[tex_off]==0:  tex_off +=1
    num_tex=data[tex_off]
    tex_off+=4
    vi= tex_off +0
    for i in range(num_tex):
        tex_data=data[vi:vi+4]
        tex_nome=data[vi+4:vi+20]
        print "%3i"%(i), toname(tex_nome), tex_data
        #textures_files.append(toname(skp_nome)) #==============
        vi+=20
        
    ktex_num= data[vi] +256*  data[vi+1]
    vi+=4
    for i in range(ktex_num):
       ktex_name= data[vi:vi+16]       
       ktex_data= data[vi+16:vi+24]
       #print data[vi:vi+24]
       #data[vi+16:vi+22]= [0,0,0,0,0,0 ]
       #data[vi+16+6] = 12
       #data[vi+16+7] = 12       
       print"%3i"%(i), toname(ktex_name,True) ,  ss(ktex_data)
       #tex_if.append( [toname(ktex_name),ktex_data+[],textures_files[ktex_data[2]][0] ]  )#=========
       vi+=24
    num_mat=data[vi]

    mlist=[]
    vi+=4
    for j in range(num_mat):
            mat_name=data[vi:vi+15]
            print "%3i"%(j),toname( mat_name ), "   ", data[vi+36], data[vi+40]
            mlist.append(toname( mat_name ))
            vi+=44

    for k in range(mn):
        matt= data[off_obj + 16*k + 14]+256*data[off_obj + 16*k +15]
        print toname(data[off_obj+4 + 16*k :  off_obj+4 + 16*k +14 ] ), "material->",  mlist[matt]      
    return data

def vob_move_obj( data,obj_name , dx,dy,dz, model=0 , wig=0):

    vlist=[]
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv    

    obj_idx=None
    for j in range(mn):
        oz= data[off_obj+j*16:off_obj+j*16+16 ]
        #print oz
        RGBA=oz[0:4]
        RGBA=[g/256.0 for g in oz[0:4]]
        name= toname(oz[4:14])
        #print name 
        if name==obj_name:
            obj_idx= j+0
            break
    if obj_idx==None:
       print "obj ", obj_name," not found"
       return data
    #remove de forma seletiva
    nfk=nf+0
    j=0
    while j < nfk:    
        fi= off_fc + j*12
        if data[fi+2]==obj_idx  and   data[fi+4]==0 :
           #delete
           k1= data[fi+6] + 256* data[fi+7]
           k2= data[fi+8] +  256* data[fi+9]
           k3= data[fi+10] + 256*  data[fi+11]
           
           if k1 < nf and k2 < nf and k3 < nf :
             if not(k1 in vlist):vlist.append(k1)
             if not(k2 in vlist):vlist.append(k2)
             if not(k3 in vlist):vlist.append(k3)

        j+=1
        
    for k in vlist:
        data= move_vertex(data,k, dx,dy,dz)
    #data[i+2],data[i+3] = to_word( nfk)
    return data
    

 

def vob_add_face(data,obj_name,v1,v2,v3,mirror=True,model=0,wig=0):
 
    i=30
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256           
    mn=data[72-14+2]
    
    off_obj= 72-14+4
    off_vi=  off_obj + 16*mn
    off_fc=  off_vi + 16* nv

    obj_idx=None
    for j in range(mn):
        oz= data[off_obj+j*16:off_obj+j*16+16 ]
        #print oz
        RGBA=oz[0:4]
        RGBA=[g/256.0 for g in oz[0:4]]
        name= toname(oz[4:14])
        #print name 
        if name==obj_name:
            obj_idx= j+0
            break
    if obj_idx==None:
       #print "obj ", obj_name," not found"
 
       #print "procurando mais provavel"
       for j in range(mn):
            oz= data[off_obj+j*16:off_obj+j*16+16 ]
            #print oz
            RGBA=oz[0:4]
            RGBA=[g/256.0 for g in oz[0:4]]
            name= toname(oz[4:14])
            #print name
            
            if name==obj_name[0:len(name)]:
                obj_idx= j+0
                #print "mais provavel ",obj_name 
                break       
       return data
    
    fd=[0 for j in range(12)]
    if mirror==False or  mirror=="SI" :
       fd[0] = 16
    elif   mirror=="FX"  :
       fd[0] = 0       
    else:
       fd[0]=1


        
    fd[1]=model+0
    fd[2]= obj_idx+0
    #fd[3]= ??? #desconhecida
    #if  mirror=="EX" :   fd[3] = random.randint(0,3)
    fd[4]= 0  #dont touch !!!
    #if  mirror=="EX" :  fd[5]=   random.randint(0,1)  
    fd[3]= 0 # random.randint(0,10)
    
    fd[6],fd[7]=to_word(v1)
    fd[8],fd[9]=to_word(v2)
    fd[10],fd[11]=to_word(v3)

    if  mirror=="FX" or mirror=="SI": 
        data[off_vi+ 16*v1] = 0
        data[off_vi+ 16*v2] = 0
        data[off_vi+ 16*v3] = 0
        
    if  mirror=="SI" and False : 
        data[off_vi+ 16*v1] =  data[off_vi+ 16*v1] & 64
        data[off_vi+ 16*v2] =  data[off_vi+ 16*v2] & 64
        data[off_vi+ 16*v3] =  data[off_vi+ 16*v3] & 64

    if  mirror=="EX"  : 
        data[off_vi+ 16*v1] = data[off_vi+ 16*v1] & 0x10
        data[off_vi+ 16*v2] = data[off_vi+ 16*v2] & 0x10
        data[off_vi+ 16*v3] = data[off_vi+ 16*v3] & 0x10

        
    for j in range(12):
        data.insert( j+off_fc + nf*12 , fd[j] )
          

        
    data[i+2],data[i+3] = to_word( nf+1)
    
    return data
        
 

def glue_vertex(vtx,fc1,fc2,dist=0.01):

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
    return fc1


def read_mesh(data, keep_list=[],vm1=[],vm2=[],obj_name="",obj_data=[] ):
    #faz a leitura do reader e informa o numero de objetos,vertices e faces

    f = lambda v, l: [v[i*l:(i+1)*l] for i in range(int(math.ceil(len(v)/float(l))))]
    
    obj_list=[]
    sh_data[0]=0
    i=0
    #if (data[0],data[1]) != (0,0):
    #    print "VOB nao original" 
    #    return None
    o_nul= data[24]
    i=30
    
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256

    
    pmo= data[i+4]
    #print ss(data[i :i+12])
    num_skp=data[47-14]
    print "LEN DATA=",len(data)
    print nv,nf,pmo,o_nul, num_skp
    i=72-14
    #if (data[i],data[i+1])!= (1,0): return None
     
    #inicio dos subobjetos
     
    mn=data[72-14+2]#+data[i+3]*256
    print "Num de sub_objetos", mn
    mi=i+4
    obj_mat=[]
    all_mat=[]
    print "OBJ NAMES"
    obj_str=[]
    data_header= data[0:mi]+[]   #========================================
    data_obj_list=[]
    #for i in range(mn):        
    #    data_obj_list=data[mi:mi+mn*16]+[] #=========================================
    
    
    for i in range(mn):
        oz= data[mi+i*16:mi+i*16+16 ]
        #print oz
        RGBA=oz[0:4]
        RGBA=[g/256.0 for g in oz[0:4]]
        name= oz[4:14]+[]
        mat=oz[14]+256*oz[15]
        obj_mat+=[( RGBA, name,mat)]
        all_mat.append(mat+0)        
        #print ">",name
        data_obj_list.append([ toname(oz[4:14]),  oz[0:4]+[], mat+0 ])
        
        #print ss(data[mi+i*16:mi+i*16+16 ])
    print "--"*10    
    #print [  o[1] for o in obj_mat ]
    vtx=[]
    fvtx=[]
    vi= mi+mn*16

    data_cp=data+[]
    
    data_vetex_list=[]
    for i in range(nv):
       data_vetex_list.append(data[vi+(i*16):vi+(16*(i+1))]+[])
    print "num vertices:",nv
    nv_mod=0
    for i in range(nv):
       a,x,y,z= read_axyz(data[vi:vi+16])
       fvtx.append(data[vi ])
       a=data[vi] #+ data[]
       vtx.append([x,y,z])
       obj_str.append("v %f %f %f \n"%(x,y,z))
       for k1 in range(len(vm1)):
           if similar_v(vm1[k1] , [x,y,z],0.001 )==True:
              #print "MOD",i 
              ndd=bin_v(vm2[k1][0],vm2[k1][1],vm2[k1][2])
              for k2 in range(len(ndd)):          data_cp[vi+k2+4]=ndd[k2]
                #print "READ",i
              if not(similar_v(vm1[k1],vm2[k1],0.01)) :
                  #print " -----------------"
                  #print [x,y,z]
                  #print  vm1[k1]
                  #print  vm2[k1]
                  nv_mod+=1              
              break      
      
       #data[vi]=4
       if data[vi  ]!=0:
           pass
           #data[vi]=4    
           #print [data[vi]& jb for jb in [1,2,4,8,16,32,64,128]  ]
           
       vi+=16    
    #print vtx[-1]
    print "changed ",nv_mod , "vertices"
    fcs=[]
    it=vi+0
    
    data_faces_list=[]
    for i in range(nf):
            data_faces_list.append( data[it:it+12] )
            it+=12


        
    fn=[ 0 for i in range(mn) ]
    vi_save=vi+0
    print "LEN DATA=",len(data)
    data_faces=data[vi:vi+(nf*12)]
    new_data_face=[]

      
    for oid in range(mn):
     for imod in range(0,12):
        wmod=0 
      #for wmod in (0,1,8):
         
        obj_str.append("\n")
        #if  keep_list.count( obj_mat[oid][1] ) == 0 :
           #print "NOT", obj_mat[oid][1]  
           #continue         
        obj_list.append(OBJETO( obj_mat[oid][1]  ) )
        obj_i=obj_list[-1]
        obj_i.color=     obj_mat[oid][0]
        obj_i.type_render=0
        obj_i.material=    toname( obj_mat[oid][1])
        #print  oid, toname( obj_mat[oid][1])
        obj_str.append("g "+ "m%i_"%(imod) +"w%i_"%(wmod)+toname( obj_mat[oid][1])+ " \n")
        obj_i.iname=   obj_mat[oid][1]
        obj_i.mat_id= obj_mat[oid][2]
        #if  keep_list.count( obj_mat[oid][1] ) == 0 :
        #    obj_i.enable=False
        obj_i.id=oid+0
        vi=vi_save+0
        face_start=vi+0        


        
        new_nf=nf+0

        
        for i in range(nf):
            oz= data[vi:vi+12]
            vi+=12 
            obj=oz[2]        
            v3,v2,v1 = oz[10]+256*(oz[11]),oz[8]+256*(oz[9] ), oz[6]+256*(oz[7])  
            #if True:
                #data[vi+7]=data[vi+7]&0x0f 
                #data[vi+9]=data[vi+9]&0x0f 
                #data[vi+11]=data[vi+11]&0x0f
                #data[vi]=0xff
                #data[vi]=data[vi]| 2
            fn[obj]+=1      

            #oz[3]==is model
            #oz[1] == car model XR,XRR, XRT
            if  oz[2]==oid and (oz[1]==imod )  and(oz[4]==0)   :
                            
              #if oid==26:
              #    print "+", oz
              #if oid==25:
              #    print "-", oz
                  
              #if oz[2]==51 or oz[2]==5 or oz[2]==5 or oz[2]==22 :
                  #print ss(oz)
              def get_xyz(vid):
                  if vid > nv:
                     vid= vid &(0x1fff)
                     xyz=vtx[vid]
                     #xyz[0]*=-1.0
                  else:
                     xyz= vtx[vid]
                  return xyz
                 
              def get_vs(vid):
                  if vid >= nv:
                     vid= vid &(0x0fff)
                  if vid>=nv:
                     print "ERR" 
                  return vid+1
                
              av1,av2,av3 =  [  get_vs(vj) for vj in (v1,v2,v3)]
              obj_str.append("f %i %i %i \n"%(av1,av2,av3))
              #print obj_str[-1]
              if False :
                     xyz1,xyz2,xyz3 = [ get_xyz(vj) for vj in (v1,v2,v3)]
                     vbin= [ data_vetex_list[get_vs(vj)][0:4] for vj in (v1,v2,v3) ]
                 
                     #if fvtx[get_vs(v1)]== fvtx[get_vs(v2)] and fvtx[get_vs(v2)]== fvtx[get_vs(v3)]  :
                     obj_i.add_face(xyz1,xyz2,xyz3,fbin=oz+[],vbin =vbin )
                     obj_i.cor=(1.0,0,0,0)
                     obj_i.type_render=1
                     if obj_i.enable:
                        new_data_face.extend([oz+[]])


    
    return ''.join(obj_str), [],[],[],[],data_cp

    #print "LEN DATA=",len(data)
    #return obj_list,data
    # faz a leitura do resto:
    all_mat.sort()
    #print all_mat
    vi+=28 # ??
    print "BG --------------------"
    vi_save=vi+0
    skp_num=data[vi]
    skp_dsc1=data[vi+1]
    #skp_dsc2=data[vi+2]
    print skp_num
    print data[vi-2:vi+6]
    vi+=4
    #print all_mat
    textures_files=[]
    for i in range(skp_num):
        skp_data=data[vi:vi+4]
        skp_nome=data[vi+4:vi+20]
        print toname(skp_nome), skp_data
        textures_files.append([toname(skp_nome), skp_data+[]] ) #==============
        vi+=20

    vi_save=vi+0
    ktex_num= skp_num=data[vi] +256*  data[vi+1]
    vi+=4
    print "_"*20
    print ktex_num
    tex_if=[]
    #
    for i in range(ktex_num):
       ktex_name= data[vi:vi+16]       
       ktex_data= data[vi+16:vi+24]
       print data[vi:vi+24]
       #data[vi+16:vi+22]= [0,0,0,0,0,0 ]
       #data[vi+16+6] = 12
       #data[vi+16+7] = 12       
       #print toname(ktex_name,True) ,ss(ktex_data),textures_files[ktex_data[2]][0] 
       #tex_if.append( [toname(ktex_name),ktex_data+[],textures_files[ktex_data[2]][0] ]  )#=========
       vi+=24

    num_mat=data[vi]
    vi+=4
    m_list=[]
    for i in range(num_mat):
        mat_name=data[vi:vi+15]
        mat_data=data[vi+15:vi+44  ]
        print toname(mat_name,True),ss(mat_data[0:6])
        m_list.append([toname(mat_name),mat_data+[]])  #===========================
        vi+=44
    #ajusta material dos objetos
    for k in obj_list:
           k.mat_id=m_list[k.mat_id][0]
           print k.material,':',k.mat_id, "nvertex:", len(k.vt ),k.color

           #if k.material[0]=='C': k.enable==False


    #update_thigs

    #data[face_start:face_start+(nf*12)] = new_data_face

    #print "CHANGE:", nf, len(new_data_face)/12
    #nf=len(new_data_face)/12
    
    #data[30],data[31]= to_word(nv) 
    #data[32],data[33]= to_word(nf)           
    return   obj_list,  data_header,data_obj_list, data_vetex_list,data_faces_list, textures_files,tex_if,m_list,data[vi:]







def gen_new_vob(header,list_obj,list_vtx,list_fcs,list_texfiles,list_tex,list_mat,data_r):

    #update_values
    #header eh um grupo de bytes

    #list_vtx: cada elemento tem 16 bytes
    
    data=header+[]    
    data[30],data[31]= to_word(len(list_vtx)) 
    data[32],data[33]= to_word(len(list_fcs))

    
    #data[72-14+2]= len(list_obj)
    
    #data[34],data[35] = to_word(len(list_texfiles))
                                        
    for i in list_obj:                                        
        data.extend(i[1]+str_to_bin(i[0],10))        
        data.extend( to_word(i[2]))
                                        
    for i in list_vtx:  data.extend(i)
    for i in list_fcs:  data.extend(i)


    #header do material
    mh=[ 0 for i in range(32)]
    mh[28],mh[29]=to_word(len(list_texfiles))
    data.extend(mh)
    for i in list_texfiles:
            data.extend(i[1]+str_to_bin(i[0],16))


    data.extend( to_word(len(list_tex))  )                                        
    data.extend( [0,0]  )
    for i in list_tex :
          data.extend(str_to_bin(i[0],16)+i[1])
                                   
 
    
    
    data.extend( to_word(len(list_mat))  )
    data.extend( [0,0]  )
    for i in list_mat :
            data.extend( str_to_bin(i[0], 15)+i[1]  )

    return data+data_r



    







def open_vob(fname,id):
    f=open(fname,"rb")
    #f.read(102)
    i=0
    vi=0
    np=[]
    vts=[]
    obj=0
    j=0
    nvv=[]
    pts=[]
    dx=0
    data=[]
    
    #for i in range(0x3b2400):
    #s_in=f.read()

    buf=f.read(512)
    while buf!="":
         for s in buf:
            data.append(struct.unpack("B",s)[0])
         buf=f.read(512)   

    
    
    #kp=[ 'GLASS',  'plastic', 'M2_mirR', 'l_ffog', 'exhst_1', 'l_brk', 'GRLL_B1', 'l_rind', 'C2_stem', 'L_RTAIL', 'GRLL_T2', 'g_head', 'light', 'g_fog', 'l_rev', 'l_fsind', 'S_plate', 'M1_SIDE', 'C1_FRNT', 'C1_TOP', 'C1_BACK', 'colum_T', 'GRILL_F', 'dash_F', 'OIL', 'MIRR_R', 'intke_R', 'handle', 'Consl_1', 'consl_2', 'gear', 'gearTOP', 'levr_R', 'dashtex']      
    incl=[]
    kp=[]
    vm1=[]
    vm2=[]
    #vm1=read_obj("D:\Documents and Settings\DrRafael\Desktop\\ex_0.obj") #base XF 
    #vm2=read_obj("D:\Documents and Settings\DrRafael\Desktop\\ex_1.obj") #moded XF
    #obj_patch= read_obj("D:\Documents and Settings\DrRafael\Desktop\\teto.obj")

    new_data=data[14:]+[]
    #le o aqruivo de trocas
    sw= open(text_file,"r" ).readlines()
    o_vt, obj=read_obj_faces_names(obj_file )
    vtab={}

    new_material(new_data, "None",[] )

    #new_data= texture_param (new_data, name , param=[000 003 000 000 024 048 000 000 ]  )
    #new_data= texture_param (new_data, "TOP", param=[000, 003, 000 ,000 ,024 ,048 ,000 ,000 ]  )    
    
    model=[True,True]
    mdst=0
    flag_mirror=True
    
    for k in range(len(o_vt)):
       
      v1,new_data=vob_add_vertex(new_data , o_vt[k][0], o_vt[k][1],o_vt[k][2] )
      vtab[k+0]=v1+0

    
    def a_matblak(x,y,z,a):
        if y/1.15 + z/1.25 > 1 : return 0,0,0
        return False    
    #new_data = clip_vertex_if( new_data, "MATBLAK",a_matblak )   
 
    
    def a_panel(x,y,z,a):
        if x > 0.65 : return x-0.05,y-0.05,z
        if  x > 0.52  and y > 0.55 and z < 0.70 : return  x,y-0.07 ,z
        if  x > 0.3 and y > 0.64  and z < 0.66 :  return x,y-0.10 ,z
 
        #if x > 0.65 : return x-0.05,y-0.05,z        
        if y  > 0.52 and z > 0.66 : return x,y-0.13, z-0.08
        return False
    #new_data = clip_vertex_if( new_data, "in_dshT",a_panel  )    
  
  
 
    for l in sw:
         
        cmd= l.split()
        if cmd==[]: continue
        if cmd[0]=='#': continue
        if cmd[0]=="mirror":
           if cmd[1].lower()=="on" :
               flag_mirror= True
               print "mirror ON"
           if cmd[1].lower()=="off" :
               flag_mirror  =False
               print "mirror OFF"
           if cmd[1].lower()=="fix" :
               print "mirror FIX"
               flag_mirror  ="FX"
           if cmd[1].lower()=="side" :
               print "mirror SIDE"
               flag_mirror  ="EX"
               
           if cmd[1].lower()=="simetry" :
               print "mirror SIMETRY"
               flag_mirror  ="SI"
               
        if cmd[0]=="glue":
           p1 =cmd[1]
           p2= cmd[2]
           print "clean model",p1,p2
           o_fc1= obj[ p1] 
           o_fc2= obj[ p2]
           obj[ p1] = glue_vertex( o_vt , o_fc1, o_fc2 , dist=0.02  )
           
           
        if cmd[0]=="clean_model":
           p1 =cmd[1] 
           print "clean model",p1  
           new_data=vob_remove_faces_model(new_data,p1 , model=mdst , wig=None)

        if cmd[0]=="new_tex_file":
           new_data= new_tex_file(new_data,cmd[1]  )

        if cmd[0]=="end":
           break 
                
        if cmd[0]=="set_texture_align":
           print "set_texture_align" 
           p1=  cmd[1]  
           p2=  cmd[2]
                
           tsize= int(cmd[3])
           torient= int(cmd[5])

           flag =int(cmd[4])
           xyz1=eval(cmd[6])
           xyz2=eval(cmd[7])
           new_data = set_tex_align(new_data,p1 , p2 , tsize, flag, torient ,xyz1,xyz2 )

        if cmd[0]=="set_material_param":
           print "set_material_param" 
           p1=  cmd[1]  
           p2=    [ float(ij ) for ij in  cmd[2:6] ]
           p3 = int(cmd[6] )
 
           new_data = set_material_param(new_data,p1 ,p2 ,p3,p3 )
           
        if cmd[0]=="clean_all":
           dnew_ata=vob_clean_all(new_data,int(cmd[1]),int(cmd[2]))
           
        if cmd[0]=="set_tex_param":
           print "Set tex param" 
           p1=  cmd[1]  
           p2= [ int(ij ) for ij in  cmd[3:] ]
           new_data = set_tex_param_material(new_data,cmd[1],cmd[2] ,p2   )
           
           #new_data= set_tex_param(new_data,cmd[1],cmd[2] ,p2  )

           
        if cmd[0]=="clean_mesh":
           p1 = int( cmd[1]) 
           print "clean mesh",p1  
           new_data=vob_remove_mesh(new_data,p1 , wig=None)
           
        if cmd[0]=="clean":
           p1 =cmd[1] 
           print "clean ",p1  
           new_data=vob_remove_faces(new_data,p1 , model=0 , wig=None)
           #new_data=vob_remove_faces(new_data,p1 , model=1 , wig=None)
           #new_data=vob_remove_faces(new_data,p1 , model=2 , wig=None)
           
        if cmd[0]=="model":
           p1 =int(cmd[1])
           mdst=p1
           print "SET MODEL TO ",mdst
##              
##           if p1==1:
##              model[1]=True
##              mdst=1
##              
##           if model==[True,True]:
##              mdst=0
##              
##        if cmd[0]=="model_off":
##           p1 =int(cmd[1])
##           if p1==0:
##              model[0]=False
##              mdst=1
##              
##           if p1==1:
##              model[1]=False
##              mdst=0
##              
##           if model==[False,False]:
##              mdst=0
              
           
        if cmd[0]=="clean_id":
           p1 =int(cmd[1]) 
           print "clean ",p1  
           new_data=vob_remove_faces_id(new_data,p1 , model=0 , wig=None)
           #new_data=vob_remove_faces_id(new_data,p1 , model=1 , wig=None)
           #new_data=vob_remove_faces_id(new_data,p1 , model=2 , wig=None)
           #new_data=vob_remove_faces_id(new_data,p1 , model=3 , wig=None)
 
            
        if cmd[0]=="move_v":
           p1,p2=cmd[1],cmd[2]  
           #print "moving ",p1, " by ",p2
           px=eval(p2)
           print px
           vob_move_obj(new_data,p1,px[0],px[1],px[2] ,model=None , wig=None)

        if cmd[0]=="copy_material":
            #print "material copy" 
            new_data= copy_material(new_data, cmd[1],cmd[2] )
             
             
            
        if cmd[0]=="obj":            
           p1,p2,p3=cmd[1],cmd[2],cmd[3]         
           print "Novo objeto ",p1
           new_data = vob_raw_obj(new_data, p1,mat=int(p2), cor=eval(p3)  )

         #remove_pts(data,obj_name, vs )

        if cmd[0]=="remove_pts":
           p1,p2=cmd[1],cmd[2]
           print "add in ",p1, " contents of ",p2+".obj"
            
           #o_vt,o_fc= read_obj_faces("D:\Documents and Settings\DrRafael\Desktop\\CLIO\\"+p2+".obj" )
           if obj.has_key(p2)==False:
                print "not found ",p2
                print 
                continue
           o_fc= obj[ p2]
           vs=[]
           for fi in   range(len(o_fc)):
               v1,v2,v3 = [ g for g in [  o_fc[fi][0] ,o_fc[fi][1] ,o_fc[fi][2] ] ]

               vs.append( [ o_vt[v1][0], o_vt[v2][1],o_vt[v3][2] ]  )
           new_data= remove_pts(new_data,p1, vs )
           
               #new_data=vob_add_face(new_data ,p1,v1,v2,v3, mirror=flag_mirror, model=mdst , wig=0 )
               #new_data=vob_add_face(new_data ,p1,v1,v2,v3, mirror=False, model=1 , wig=0 )

               
         
        if cmd[0]=="add":
           p1,p2=cmd[1],cmd[2]
           print "add in ",p1, " contents of ",p2+".obj"
            
           #o_vt,o_fc= read_obj_faces("D:\Documents and Settings\DrRafael\Desktop\\CLIO\\"+p2+".obj" )
           if obj.has_key(p2)==False:
                print "not found ",p2
                print 
                continue
           o_fc= obj[ p2]           
           for fi in   range(len(o_fc)):
               v1,v2,v3 = [ vtab[g] for g in [  o_fc[fi][0] ,o_fc[fi][1] ,o_fc[fi][2] ] ]
               new_data=vob_add_face(new_data ,p1,v1,v2,v3, mirror=flag_mirror, model=mdst , wig=0 )
               #new_data=vob_add_face(new_data ,p1,v1,v2,v3, mirror=False, model=1 , wig=0 )
             

        if cmd[0]=="replace":
           p1,p2=cmd[1],cmd[2]
           print "change ",p1, "by contents of ",p2+".obj"
           #o_vt,o_fc= read_obj_faces("D:\Documents and Settings\DrRafael\Desktop\\CLIO\\"+p2+".obj" )
           if obj.has_key(p2)==False:
                print "not found ",p2
                print 
                continue
           o_fc= obj[ p2]
   
  
           #vlista = vob_vertex_list(new_data)
      
##           for k in range(len(o_vt)):
##               g= get_near( vlista , o_vt[k][0], o_vt[k][1],o_vt[k][2] )
##               
##               if g==None:
##                  v1,new_data=vob_add_vertex(new_data , o_vt[k][0], o_vt[k][1],o_vt[k][2] )
##                  vtab[k+0]=v1+0
##               else:
##                  vtab[k+0]=g+0

                  
##           for k in range(len(o_vt)):
##               v1,new_data=vob_add_vertex(new_data , o_vt[k][0], o_vt[k][1],o_vt[k][2] )
##               vtab[k+0]=v1+0
           #if model==[True,True]:
           #    new_data=vob_remove_faces(new_data,p1 , model=0 , wig=None)
               #new_data=vob_remove_faces(new_data,p1 , model=1 , wig=None)
               #new_data=vob_remove_faces(new_data,p1 , model=2 , wig=None)
           #else:    
           new_data=vob_remove_faces(new_data,p1 , model=mdst , wig=None)
           #new_data=vob_remove_faces(new_data,p1 , model=1 , wig=None)
           #new_data=vob_remove_faces(new_data,p1 , model=1 , wig=None)
           
           for fi in   range(len(o_fc)):
               v1,v2,v3 = [ vtab[g] for g in [  o_fc[fi][0] ,o_fc[fi][1] ,o_fc[fi][2] ] ]
               new_data=vob_add_face(new_data ,p1,v1,v2,v3, mirror=flag_mirror, model=mdst , wig=0 )
               
               #new_data=vob_add_face(new_data ,p1,v1,v2,v3, mirror=False, model=1 , wig=0 )
    #o_vt,o_fc= read_obj_faces("D:\Documents and Settings\DrRafael\Desktop\\CLIO\side_clio.obj")
    
##    #obj_name="m1_w2_C1_frnt"
##    #m3_w1_barsSHNY
##    #new_data=data[14:]+[]
##
##    
##    #adiciona os vertices e gera a tabela
##    vtab={}
##    for k in range(len(o_vt)):
##       #v1,new_data=vob_add_vertex(new_data , o_vt[k][0], o_vt[k][1],o_vt[k][2] )
##       #vtab[k+0]=v1+0
##       pass
##    #new_data=vob_remove_faces(new_data,"C1_frnt" , model=1 , wig=2)
##    
##    for fi in   range(len(o_fc)):
##       #print  o_fc[fi]
##       #v1,v2,v3 = [ vtab[g] for g in [  o_fc[fi][0] ,o_fc[fi][1] ,o_fc[fi][2] ] ]       
##       #new_data=vob_add_face(new_data ,"barsSHNY",v1,v2,v3, mirror=True, model=1 , wig=2 )
##       pass
    

 

    #new_data = clip_vertex(new_data ,400,1.95,400)
    
    #new_data = scale_vertex(new_data ,1.0,  1.0 -0.08/1.51,1.0)

    
    
    print "length in:",len(data)
    print "done"
    #obj_str,data_header, list_obj, list_vtx, list_fcs,new_data = read_mesh(data[14:],kp,vm1,vm2)
    #print "gravando OBJ"
    #open("D:\Documents and Settings\DrRafael\Desktop\\XF.obj",'w').write(obj_str)
    
    

    f=open(vob_saida,"wb")
    for x in data[0:14]:
       f.write(struct.pack("B",x) )       
    for x in new_data:

         f.write(struct.pack("B",x) )
  
    return None



    #print vts[0].add_data( [],[],[],[] )    
 
    for x in data[0:14]:
       f.write(struct.pack("B",x) )

    #dout= gen_new_vob(data_header,list_obj,list_vtx,list_fcs,list_texfiles,list_tex,list_mat,data_r)

    l_obj,l_vt,l_fc=[],[],[]
    
    for k in vts:
       l_obj,l_vt,l_fc,nada= k.add_data(l_obj,l_vt,l_fc,list_mat )
       
    #print l_obj[0],l_vt[0],l_fc[0]

    #list_obj,list_vtx,list_fcs ,nada= vts[51].add_data(list_obj,list_vtx,list_fcs,list_mat )
    #dout= gen_new_vob(data_header,l_obj,l_vt,l_fc, list_texfiles,list_tex,list_mat,data_r) 
    dout= gen_new_vob(data_header,list_obj,list_vtx,list_fcs, list_texfiles,list_tex,list_mat,data_r)   
        
    
    for x in dout:
       try: 
         f.write(struct.pack("B",x) )
       except:
         print x
         jfkdjk()
    f.close
    return vts 
    print "length out:",len(dout) 
    #sys.exit()
   



        
def waite():
    return
def main():
        global window
        global ff
        global vv
        global sh_data

        sh_data={}
        
        ff=[]
        vv=  open_vob(vobname,12)
        return 
 
main()

        
#sys.exit(0) 

