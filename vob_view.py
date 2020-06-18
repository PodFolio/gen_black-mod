

import struct
import math
import Image
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
uniqueNumberInternal = 0



mesh_id= 1

global textures_gl
textures_gl={}


vobname= "C:\\Blackwood.wld"


def uniqueNumber():
    global uniqueNumberInternal
    uniqueNumberInternal += 1
    return uniqueNumberInternal

def unpackColor(x):
    return (ord(x[1])/255.0,ord(x[2])/255.0,ord(x[3])/255.0,(255-ord(x[0]))/255.0)

def next_p2 (num):
	""" If num isn't a power of 2, will return the next higher power of two """
	rval = 1
	while (rval<num):
		rval <<= 1
	return rval

    
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

def znormal(p1,p2,p3):
    d1=p3[0]-p1[0],p3[1]-p1[1],p3[2]-p1[2]
    d2=p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]
    x=d1[1]*d2[2]- d1[2]*d2[1]
    y=d1[0]*d2[2]- d1[2]*d2[0]
    z=d1[1]*d2[0]- d1[0]*d2[1]
    #nnz= math.sqrt( x*x+y*y+z*z)

    #if nnz==0: nnz =1.0
    nnz=1.0
    return x/nnz,y/nnz,z/nnz


def direct(p1,p2,p3):
    z = znormal(p1,p2,p3)
    k =math.atan2(z[0],z[1])
    w =math.atan2(z[2], math.sqrt(z[1]* z[1]  +z[0]* z[0]) )
    return k, w     
    
def toname(d,fill=False):
    s=""
    for k in d:
        if k==0:
           if fill:
              s+=" "  
           else:
              return s
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
        
def to_word(x):
            return x&0xff, (x&0xff00)/256
#classes basicas

def BuildTexture (path):
	""" // Load Image And Convert To A Texture
	path can be a relative path, or a fully qualified path.
	returns False if the requested image couldn't loaded as a texture
	returns True and the texture ID if image was loaded
	"""
	# Catch exception here if image file couldn't be loaded
	try:
		# Note, NYI, path specified as URL's could be access using python url lib
		# OleLoadPicturePath () supports url paths, but that capability isn't critcial to this tutorial.
		Picture = Image.open (path)
	except:
		print "Unable to open image file '%s'." % (path)
		return False, 0

	glMaxTexDim = glGetIntegerv (GL_MAX_TEXTURE_SIZE)
	glMaxTexDim = 512
	WidthPixels = Picture.size [0]
	HeightPixels = Picture.size [1]

	if ((WidthPixels > glMaxTexDim) or (HeightPixels > glMaxTexDim)):
		# The image file is too large. Shrink it to fit within the texture dimensions
		# support by our rendering context for a GL texture.
		# Note, Feel free to experiemnt and force a resize by placing a small val into
		# glMaxTexDim (e.g. 32,64,128).
		if (WidthPixels > HeightPixels):
			# Width is the domainant dimension.
			resizeWidthPixels = glMaxTexDim
			squash = float (resizeWidthPixels) / float (WidthPixels)
			resizeHeightPixels = int (HeighPixels * squash)
		else:
			resizeHeightPixels = glMaxTexDim
			squash = float (resizeHeightPixels) / float (HeightPixels)
			resizeWidthPixels = int (WidthPixels * squash)
	else:
		# // Resize Image To Closest Power Of Two
		if (WidthPixels > HeightPixels):
			# Width is the domainant dimension.
			resizeWidthPixels = next_p2 (WidthPixels)
			squash = float (resizeWidthPixels) / float (WidthPixels)
			resizeHeightPixels = int (HeighPixels * squash)
		else:
			resizeHeightPixels = next_p2 (HeightPixels)
			squash = float (resizeHeightPixels) / float (HeightPixels)
			resizeWidthPixels = int (WidthPixels * squash)
		# 
	# Resize the image to be used as a texture.
	# The Python image library provides a handy method resize (). 
	# Several filtering options are available.
	# If you don't specify a filtering option will default NEAREST
	#Picture = Picture.resize ((resizeWidthPixels, resizeHeightPixels), Image.BICUBIC)
	Picture = Picture.resize ((resizeWidthPixels, resizeHeightPixels))	
	lWidthPixels = next_p2 (resizeWidthPixels)
	lHeightPixels = next_p2 (resizeWidthPixels)
	# Now we create an image that has the padding needed
	newpicture = Image.new ("RGB", (lWidthPixels, lHeightPixels), (0, 0, 0))
	newpicture.paste (Picture)

	# Create a raw string from the image data - data will be unsigned bytes
	# RGBpad, no stride (0), and first line is top of image (-1)
	#pBits = newpicture.tostring("raw", "RGBX", 0, -1)
	pBits = newpicture.tostring("raw", "RGBX", 0, -1)	

	# // Typical Texture Generation Using Data From The Bitmap
	texid = glGenTextures(1);											# // Create The Texture
	glBindTexture(GL_TEXTURE_2D, texid);								# // Bind To The Texture ID
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST  );		# // (Modify This For The Type Of Filtering You Want)
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST  );     # // (Modify This For The Type Of Filtering You Want)

	# // (Modify This If You Want Mipmaps)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, lWidthPixels, lHeightPixels, 0, GL_RGBA, GL_UNSIGNED_BYTE, pBits);

	# Cleanup (python actually handles all memory for you, so this isn't necessary)
	# // Decrements IPicture Reference Count
	Picture = None
	newpicture = None
	return True, texid					# // Return True (All Good)





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

        
        self.mat_data=[]
        self.mat_quad=[]
        self.tex_data=[]
        
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
            
            fbin[0]=self.fflags[i][0]  #MIRROR?
            fbin[1]=self.fflags[i][1]   # qual modelo de carro
            #fbin[2]=self.fflags[i][2]     OID       
            fbin[3]=self.fflags[i][3]
            fbin[4]=self.fflags[i][4]  # 0= mesh
            #fbin[5]=self.fflags[i][5] #controla as normais ?
            list_fcs.append(fbin)
            
        return list_obj,list_vtx,list_fcs,list_mat
    
    def geo_render(self):
         for f in range( len(self.fc) ):
           if   self.fflags[f][4]!=0 :
               continue

           if self.fflags[f][1] in (0,2, ) :
                pass
           else:
                pass
                #ontinue
            
           if self.fflags[f][0]==0: 
              #glColor3f( random.random(),random.random(), random.random()  )
              #glColor3f(1,0,0)
              pass
           else:
              #glColor3f(1,1,1)
              pass
               
           if self.fflags[f][3] ==2     :
               #glColor3f(1.0,0.2,0.2)
               pass
           #if self.fflags[f][0] ==0  :   glColor3f(0.2,0.2,0.1)            
           if self.fflags[f][5] > 1  :
               #glColor3f(0.2,1,0.2)
               pass
           else:
               
              #glColor3fv(self.color[0:3])
               glColor3f(1,1,1)
           glColor3f(1,1,1)   
           for vi in self.fc[f]:
              #print  self.vflags[vi]
              #if   self.vflags[vi][0] & 64 !=0  :glColor3f( 1,0,1  )
              #if   self.vflags[vi][0] & 32 !=0  :glColor3f( 1,1,0  )
              #if   self.vflags[vi][0] & 16 !=0  :glColor3f( 0.5,0.5,0.9  )
              if self.vflags[vi][0]  >127:
                #glColor3f( 0.2,1,0.2  )
                pass 
              else:
                 pass
                 #glColor3f( 0.5,0.5,0.5  )
           
              #glVertex3fv( self.vt[ vi ]  )
           
           #if self.fflags[f][0]   & 16 == 0:



              
           if self.fflags[f][0]    != 990 :
               
             glNormal3f (self.nv[f][0] , self.nv[f][1],self.nv[f][2] )
             
             if  True:
                for vi in self.fc[f]:                 
                     
                   side=0
                   ixu , ixv = 0,1

                   
                   if  self.mat_data[1]==5:  #top
                       ixu , ixv = 0,1
                   elif  self.mat_data[1]==3 :   #side               
                       ixu , ixv = 1,2
                       
                   elif  self.mat_data[1]==2 :   #back               
                       ixu , ixv = 0,2
                       
                   elif  self.mat_data[1]==1 :     #front             
                       ixu , ixv = 0,2

                       
                   elif  self.mat_data[1]==4 :     #door interior             
                       ixu , ixv = 1,2
                       
                       
                   uv_flag= self.tex_data[side][1][1]
                   xu=0
                   xv=0
                   if  self.mat_quad[1] != self.mat_quad[0]:                        
                      xu= ( self.vt[ vi ][ixu]  - self.mat_quad[0] )/(self.mat_quad[1]-self.mat_quad[0])
                   if self.mat_quad[3]!= self.mat_quad[2]:
                      xv= ( self.vt[ vi ][ixv]  - self.mat_quad[2] )/(self.mat_quad[3]-self.mat_quad[2])

                   if  self.mat_data[1]==1 :                       
                       #xu= 1-xu
                       pass
                   elif  self.mat_data[1]==2 :
                       #xu,xv= xv,xu
                       pass
                   elif  self.mat_data[1]==2 :
                       #xu,xv= xv,xu
                       pass
                   elif  self.mat_data[1]==5 :                       
                       #xv= 1-xv
                       #xu,xv=xv,xu
                       pass

                       
                   if abs(xu) >1 or abs(xv) > 1 :
                       #print  "ERR ",xu,xv
                       #nada()
                       pass
                   #uv =[ du, dv , u0,v0  ]
                   #uv=[self.tex_data[side][1][4],self.tex_data[side][1][5],self.tex_data[side][1][6],self.tex_data[side][1][7]]

                   du,dv=self.tex_data[side][1][4]+0,self.tex_data[side][1][5]+0
                   u0,v0=self.tex_data[side][1][6]+0,self.tex_data[side][1][7]+0
                   
                   tu = xu * (  du/ 64.0 ) + u0/ 64.0 
                   tv = xv * ( dv/ 64.0 ) + v0/ 64.0                  
                         
                   if uv_flag == 0:
                       tu = xu * (  du/ 64.0 ) + u0/ 64.0 
                       tv = 1- (xv * (  dv/ 64.0 )+  v0/ 64.0)
                       tv=1-tv
                       
                   elif uv_flag == 1: #front  x,z
                       #du,dv=dv,du
                       tv = xu *   ( du/ 64.0 ) - u0/ 64.0 
                       tu = 1- (xv *   ( dv/ 64.0 ) + v0/ 64.0)                        
                       tv=1-tv
                       
                       
                   elif uv_flag == 2:
                       tu = xu * (du/ 64.0 ) + u0/ 64.0 
                       tv = xv * ( dv/ 64.0 ) + v0/ 64.0                      # du = -du
                       
                   elif uv_flag == 3: #top/back
                       #du ,dv= dv,du
                       #u0,v0= v0,u0
                       tv =  xu * ( du/ 64.0 )   + u0/ 64.0
                       tu =  xv * ( dv/ 64.0 )   + v0/ 64.0
                       tv=  1-tv
                       #if self.tex_data[side][0]=="top":
                          #print  "%4f %4f %4f %4f"%(xu, xv, 64*tu,64*tv)
                          #glTexCoord2f(tu,  tv)
                   elif uv_flag == 4:   #side    
                       #u0=-u0                 
                       tu = 1-(xu * ( du/ 64.0 ) +u0/ 64.0)
                       tv = 1-(xv * ( dv/ 64.0 ) + v0/ 64.0)
                       if self.tex_data[side][1][0] ==1000 :
                          tu = ((xu) * ( du/ 64.0 ) +u0/ 64.0)
                       tv=1-tv


                                                                                     
                   glTexCoord2f(tu,  tv)
                   glVertex3f( self.vt[ vi ][0],self.vt[ vi ][1], self.vt[ vi ][2]    )
                    
             else:
                   p1,p2,p3=  self.fc[f]
                   glVertex3f( -self.vt[ p1 ][0],self.vt[ p1][1], self.vt[ p1 ][2]    )
                   glVertex3f( -self.vt[ p2 ][0],self.vt[ p2 ][1], self.vt[ p2 ][2]    )
                   
                   glVertex3f( -self.vt[ p2 ][0],self.vt[p2 ][1], self.vt[ p2 ][2]    )
                   glVertex3f( -self.vt[ p3 ][0],self.vt[ p3 ][1], self.vt[ p3 ][2]    )
                   

                   glVertex3f( -self.vt[ p3 ][0],self.vt[ p3 ][1], self.vt[ p3 ][2]    )
                   glVertex3f( -self.vt[ p1 ][0],self.vt[ p1][1], self.vt[ p1 ][2]    )                
              
    def render(self ):

           #k.mat_data= m_list[k.mat_num_id ][1]+[]           
           #k.mat_quad= [   fixed(k.mat_data[5+4*(tmp):5+4*(tmp+1) ]) for tmp in range(4) ] 
           #k.tex_data= [ tex_if[ k.mat_data[40-15] ], tex_if[ k.mat_data[36-15] ] ]
           #k.tex_files = textures_files  +[]
           
           global texures_gl
           #self.geo_render()
           #return
           if self.enable==False:
               return
           if len(self.fc)==0: return

            
           tf_id= self.tex_data[0][1][2]
           
           fname= self.tex_files[tf_id]
           #print textures_gl
           if True:
               if  textures_gl.has_key( fname ):
                  if  textures_gl[fname] !=None :
                    glEnable(GL_TEXTURE_2D);            
                    glBindTexture(GL_TEXTURE_2D, textures_gl[fname] )
                  else:
                     glDisable(GL_TEXTURE_2D);
               else:
                  xfname=fname+"" 
                  if fname=="DEFAULT":
                      xfname="HEL_DEFAULT"
                  status,tid= BuildTexture( "veh\\"+xfname+".jpg" )
                  #status,tid    = False,0
                  if status==False:
                       print "TEXTURE ",fname, " NOT FOUND"
                       #raise NameError
                       textures_gl[fname]=None
                  else:   textures_gl[fname]=tid+0
                       
               #glDisable(GL_TEXTURE_2D);

           
           glColor3fv(self.color[0:3])
           #glMaterialfv(GL_FRONT,GL_DIFFUSE,self.color)
           #glDisable(GL_LIGHTING)
           #glEnable(GL_LIGHTING)
           #glEnable(GL_CULL_FACE)         

              
           if (self.GLcalllist is None):
                self.GLcalllist = glGenLists(1)
                glNewList(self.GLcalllist, GL_COMPILE)                
                self.geo_render()
                glEndList()

           
           
   
 	
           if self.type_render==1:
              glBegin(GL_TRIANGLES) 
              #glBegin(GL_LINES)
              #glBegin(GL_POINTS)
              pass
           else:
              glBegin(GL_TRIANGLES)
              #glBegin(GL_LINES)
              #glBegin(GL_POINTS)
              #glBegin(GL_LINE_STRIP)
              pass
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

    dsz= len(data)
    while start==False:
        start=True
        i+=1
        if i > len(data):
             print "end of file ",i 
             return None,None
            
        nv=data[i] + data[i+1]*256
        nf=data[i+2] + data[i+3]*256           
        mn=data[i+30]  # offset 60

        if  mn<1  or nv <3 or nf < 9    :
            #print "null ojs ",i
            start=False
            continue
        
        if start==False: continue
        
        off_obj= i+32  # offset 62
        
        #testa os objetos, cada objeto deve ter a primeira letra valida
        #print "--------------------------"
        for k in range(mn):
            for s in range(1):
              name= data[off_obj +4 + 16*k  + s  ]
              if  name> 150 or name < 10:
                  start=False
                  break                
            if start==True :
               print toname( data[off_obj+4 + 16*k :  off_obj+4 + 16*(k+1) ] )
               pass
        if start==False: continue

        print "OK.. pass ", i
        
        off_vi=  off_obj + 16*mn
        off_fc=  off_vi + 16* nv
        face_end= off_fc + nf*12

        if face_end > dsz : continue 
        if off_vi > dsz : continue
        if off_fc > dsz : continue 
        
        #testa os vertices
        
        for k in range(nv):  
            kv= k*16 + off_vi
            a,x,y,z= read_axyz(data[kv :kv +16])
            if   data[kv+2]>0 or data[kv+3]>0 :
               #print "vertex err " 
               start=False
               break
            
            if abs(x)> 6 or abs(y) > 6:
               #start=False
               break
            
        for k in range(nf):
            kf= k*12 + off_fc
            
            if data[kf+2] > mn  or   data[kf+10]+256*(data[kf+11] & 0x0f  )> nf     :
               #print "face err " 
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
                  #break
                  pass
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
        print "-----"*4    
        print "found ", i
        print "  NVERTEX ",nv
        print "  NFACES ",nf
        print "  NOBJS ",mn
        print " next ", vi
        return i,vi
    
    ruit()
                   
def read_mesh(data, keep_list=[] ):
    #faz a leitura do reader e informa o numero de objetos,vertices e faces
    global mesh_id

    #jump the n mesh
    n=mesh_id
    #n=1
    vnext=0
    vprox=0
    while n >0:
         n=n-1
         vnext, vprox =find_header(data,vprox )

         
        
    #vnext, vprox = find_header( data,1 )
    #vnext=30
    f = lambda v, l: [v[i*l:(i+1)*l] for i in range(int(math.ceil(len(v)/float(l))))]
    cp_data=data+[]
    
    obj_list=[]
    sh_data[0]=0
     
    
    #if (data[0],data[1]) != (0,0):
    #    print "VOB nao original" 
    #    return None
    o_nul= data[24]
    #i=30
    i= vnext 

    
    nv=data[i] + data[i+1]*256
    nf=data[i+2] + data[i+3]*256

 
    
    pmo= data[i+4]
    #print ss(data[i :i+12])
    #num_skp=data[47-14   ]
    print "LEN DATA=",len(data)
    print nv,nf,pmo,o_nul 
 
    #if (data[i],data[i+1])!= (1,0): return None
     
    #inicio dos subobjetos
     
    mn=data[i+30]#+data[i+3]*256
                 
    print "Num de sub_objetos", mn
    mi=i+32
    obj_mat=[]
    all_mat=[]
    print "OBJ NAMES"
    
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
        print ">", toname(name)
        data_obj_list.append([ toname(oz[4:14]),  oz[0:4]+[], mat+0 ])
        
        #print ss(data[mi+i*16:mi+i*16+16 ])
    print "--"*10    
    #print [  o[1] for o in obj_mat ]
    vtx=[]
    fvtx=[]
    vi= mi+mn*16

    
    data_vetex_list=[]
    for i in range(nv):
       data_vetex_list.append(data[vi+(i*16):vi+(16*(i+1))]+[])
    
    for i in range(nv):
       a,x,y,z= read_axyz(data[vi:vi+16])
       fvtx.append(data[vi ])
       a=data[vi] #+ data[]
       vtx.append([x,y,z])
       #data[vi]=4
       
       if data[vi]&64 !=0 :
           pass
           #print data[vi], x,y,z
           cp_data[vi]=0
           #vtx[-1][0] =  -vtx[-1][0]
           #print [data[vi]& jb for jb in [1,2,4,8,16,32,64,128]  ]
           
       vi+=16    
    #print vtx[-1]

    fcs=[]
    it=vi+0
    
    data_faces_list=[]
    for i in range(nf):
            data_faces_list.append( data[it:it+12] )
            if data[it+5]>1 : cp_data[it]=0
            it+=12
             

        
    fn=[ 0 for i in range(mn) ]
    vi_save=vi+0
    print "LEN DATA=",len(data)
    data_faces=data[vi:vi+(nf*12)]
    new_data_face=[]

    nacc=[]
    for oid in range(mn):
        #if  keep_list.count( obj_mat[oid][1] ) == 0 :
           #print "NOT", obj_mat[oid][1]  
           #continue         
        obj_list.append(OBJETO( obj_mat[oid][1]  ) )
        obj_i=obj_list[-1]
        obj_i.color=     obj_mat[oid][0]
        obj_i.type_render=0
        obj_i.material=    toname( obj_mat[oid][1])
        obj_i.iname=   obj_mat[oid][1]
        obj_i.mat_id= obj_mat[oid][2]
        #if  keep_list.count( obj_mat[oid][1] ) == 0 :
        #    obj_i.enable=False
        obj_i.id=oid+0
        vi=vi_save+0
        face_start=vi+0        
        ngroup=[] 

        
        new_nf=nf+0

        
        for i in range(nf):
            oz= data[vi:vi+12]+[]
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

            
            if  oz[2]==oid and (  oz[1]!=199  )  and oz[1] >-1   :
              if oz[4]==0:  
                  #cp_data[vi+1-12]= random.randint( 0,3)  # tem haver com o modelo de carro
                  #cp_data[vi+3-12]= random.randint( 8,10)  # tem haver com o peso/inercia
                  #cp_data[vi+5-12]= random.randint( 1,4)
                  pass
              if not(oz[5] in ngroup ):
                 ngroup.append(oz[5])
              if obj_i.material=="M1_side":
                   #print ss(oz)
                   pass
              if obj_i.material=="M2_Bonn":
                  #print ss(oz)
                  pass
              #if obj_i.material=="C1_GTRT" or obj_i.material== "C1_splr" or oz[1]==5:
              
              #print oz[0:6]  
              #if   oz[4] & 0x0f == 0 :
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
                  if vid > nv:
                     vid= vid &(0x1fff)   
                  return vid             
               
                  
              if True :
                     xyz1,xyz2,xyz3 = [ get_xyz(vj) for vj in (v1,v2,v3)]
                     vbin= [ data_vetex_list[get_vs(vj)][0:4] for vj in (v1,v2,v3) ]
                     if   obj_i.material=="in_dshT" or obj_i.material=="cM1_side" or  obj_i.material=="xM2_Bonn" or obj_i.material=="C1_top":
                       #print ss(oz[0:7]) , vbin[0][0:4],vbin[1][0:4],vbin[1][0:4],xyz1[0], xyz2[0]
                       if  oz[5]==6  :
                         #print "--------------"
                         pass 
                         #
                         #zn= znormal(xyz1,xyz2,xyz3)
                         #lz = math.sqrt(zn[0]*zn[0]+ zn[1]*zn[1] + zn[2]*zn[2])

                         #print lz
                         
                         #nacc.append( [xyz1[0],xyz1[1],xyz1[2] ] )
                         #print oz[5], zn
                         #print math.atan2( xyz1[1], xyz1[0]  ) 
                         
                     #if fvtx[get_vs(v1)]== fvtx[get_vs(v2)] and fvtx[get_vs(v2)]== fvtx[get_vs(v3)]  :
                     obj_i.add_face(xyz1,xyz2,xyz3,fbin=oz+[],vbin =vbin+[] )
                     obj_i.cor=(1.0,0,0,0)
                     obj_i.type_render=1
                     if obj_i.enable:
                        new_data_face.extend([oz+[]])

        mx= sum([n[0] for  n in nacc ])
        my= sum([n[1] for  n in nacc])
        mz= sum([n[2] for  n in nacc])
        lz=len(nacc)+0.0
        if len(nacc )>0:
           print "media: ",  mx/lz ,my/lz ,mz/lz
        nacc=[]   
        print "flags ", "%12s "%(obj_i.material), ngroup

        
    data=cp_data+[]
    #print "LEN DATA=",len(data)
    #return obj_list,data
    # faz a leitura do resto:
    all_mat.sort()
    print all_mat
    print "offset", vi+14
    #vi+=28 # ??        #uai ! isso eh opcional ?
    print "BG --------------------"
    vi_save=vi+0
    while data[vi]==0:
         
        vi+=1
    print "jmp ",vi-vi_save
    print "face_off ", face_start
    print "end_face ", face_start + nf* 12
    print "mat num", vi
    
    skp_num=data[vi]
    skp_dsc1=data[vi+1]
    #skp_dsc2=data[vi+2]

    
    print "skp_num",skp_num
    print data[vi-2:vi+6]
    vi+=4
    #print all_mat
    textures_files=[]
    for i in range(skp_num):
        skp_data=data[vi:vi+4]
        skp_nome=data[vi+4:vi+20]
        #print  "%02i"%(i),toname(skp_nome), ss(skp_data)
        textures_files.append(toname(skp_nome)) #==============
        vi+=20
    print textures_files


 
    
    vi_save=vi+0
    ktex_num= skp_num=data[vi] +256*  data[vi+1]
    vi+=4
    print "_"*20
    print ktex_num
    tex_if=[]
    #
    print "\nTexture data"
    for i in range(ktex_num):
       ktex_name= data[vi:vi+16]       
       ktex_data= data[vi+16:vi+24]
       #print data[vi:vi+24]
       #data[vi+16:vi+22]= [0,0,0,0,0,0 ]
       #data[vi+16+6] = 12
       #data[vi+16+7] = 12       
       print "%02i"%(i) ,toname(ktex_name,True) , "@" ,ss(ktex_data), textures_files[ktex_data[2] ]
       tex_if.append( [toname(ktex_name),ktex_data+[],textures_files[ktex_data[2]] ]  ) 
       vi+=24

    num_mat=data[vi]
    vi+=4
    m_list=[]
    print "Material Data"
    for i in range(num_mat):
        mat_name=data[vi:vi+15]
        mat_data=data[vi+15:vi+44  ]
        print toname(mat_name,True) ,    ss(data[vi+10:vi+44 ]) 
        #print toname(mat_name,True)

        soo=""
        for tmp in range(4):
            soo+="%4.3f  "%(  fixed(mat_data[5+4*(tmp):5+4*(tmp+1)]) )
        print  toname(mat_name,True),soo   

        m_list.append([toname(mat_name),mat_data+[]])  #==,=========================
        vi+=44
    #ajusta material dos objetos
    print "Materials"    
    for k in obj_list:
           k.mat_num_id= k.mat_id 
           k.mat_id=m_list[k.mat_id][0]

 
           k.mat_data= m_list[k.mat_num_id ][1]+[]           
           k.mat_quad= [   fixed(k.mat_data[5+4*(tmp):5+4*(tmp+1) ]) for tmp in range(4) ] 
           k.tex_data= [ tex_if[ k.mat_data[40-15] ], tex_if[ k.mat_data[36-15] ] ]
           k.tex_files = textures_files  +[]
           #print  "%02i"%(i),k.material,':',k.mat_id,k.mat_num_id, "nvertex:", len(k.vt ),"Color=",[int(l*256) for l in k.color]

           #if k.material[0]=='C': k.enable==False


    #update_thigs

    #data[face_start:face_start+(nf*12)] = new_data_face

    #print "CHANGE:", nf, len(new_data_face)/12
    #nf=len(new_data_face)/12
    
    #data[30],data[31]= to_word(nv) 
    #data[32],data[33]= to_word(nf)           
    return   obj_list,  data_header,data_obj_list, data_vetex_list,data_faces_list, textures_files,tex_if,m_list,data[vi:],cp_data







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

    kp=['levr_L', 'wndsrnb', 'TURBO', 'TEMP', 'FUEL', 'REVS', 'SPEEDO', 'TTL_BLK',     'Under', 'Bar_R', 'glass2', 'red', 'G_winds', 'plastic', 'levr', 'trim3', 'l_head', 'metal', 'l_find', 'M2_mirR', 'l_ffog', 'exhst_1', 'l_brk', 'GRLL_B1', 'l_rind', 'C2_stem', 'L_RTAIL', 'GRLL_T2', 'g_head', 'light', 'g_fog', 'l_rev', 'l_fsind', 'S_plate', 'M1_SIDE', 'C1_FRNT', 'C1_TOP', 'C1_BACK', 'colum_T', 'GRILL_F', 'GRLL_T1', 'engine', 'GRLL_BO', 'dash_T', 'DOOR', 'floorMT', 'steel', 'dash_F', 'OIL', 'MIRR_R', 'intke_R', 'DOOR3', 'handle', 'Consl_1', 'consl_2', 'gear', 'gearTOP', 'levr_R', 'colum_F', 'colum_S', 'dashtex']

    #keep list
    kp=[ 'TURBO', 'TEMP', 'FUEL', 'REVS', 'SPEEDO', 'TTL_BLK',  'floor_R',  'metal', 'M1_SIDE', 'C1_FRNT', 'C1_TOP', 'C1_BACK', 'DOOR',  'steel', 'dash_F', 'OIL',   'DOOR3',  'Consl_1', 'consl_2', 'gear', 'gearTOP',   'colum_F', 'colum_S' ]

    #kp=[ 'GLASS',  'plastic', 'M2_mirR', 'l_ffog', 'exhst_1', 'l_brk', 'GRLL_B1', 'l_rind', 'C2_stem', 'L_RTAIL', 'GRLL_T2', 'g_head', 'light', 'g_fog', 'l_rev', 'l_fsind', 'S_plate', 'M1_SIDE', 'C1_FRNT', 'C1_TOP', 'C1_BACK', 'colum_T', 'GRILL_F', 'dash_F', 'OIL', 'MIRR_R', 'intke_R', 'handle', 'Consl_1', 'consl_2', 'gear', 'gearTOP', 'levr_R', 'dashtex']      
    incl=[]
    kp=[]
    print "length in:",len(data)    
    vts,   data_header, list_obj,list_vtx,list_fcs,list_texfiles,list_tex,list_mat ,data_r ,new_data = read_mesh(data[14:],kp )
    print  "@:",list_obj[0]
    
    f=open("helmet.sre","wb")

    #print vts[0].add_data( [],[],[],[] )    
 
    for x in data[0:14]:
       f.write(struct.pack("B",x) )
    for x in new_data:
       f.write(struct.pack("B",x) )

    f.close()

    print "OK"
    
    #dout= gen_new_vob(data_header,list_obj,list_vtx,list_fcs,list_texfiles,list_tex,list_mat,data_r)

    l_obj,l_vt,l_fc=[],[],[]
    
    for k in vts:
       l_obj,l_vt,l_fc,nada= k.add_data(l_obj,l_vt,l_fc,list_mat )
       
    #print l_obj[0],l_vt[0],l_fc[0]

    #list_obj,list_vtx,list_fcs ,nada= vts[51].add_data(list_obj,list_vtx,list_fcs,list_mat )
    #dout= gen_new_vob(data_header,l_obj,l_vt,l_fc, list_texfiles,list_tex,list_mat,data_r) 
    #dout= gen_new_vob(data_header,list_obj,list_vtx,list_fcs, list_texfiles,list_tex,list_mat,data_r)   
        
    
##    for x in dout:
##       try: 
##         f.write(struct.pack("B",x) )
##       except:
##         print x
##         jfkdjk()
##    f.close
    return vts

    print "length out:",len(dout) 
    #sys.exit()
   

def DrawGLScene():     
    global rtri
    global ff
    global vv
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); # Clear The Screen And The Depth Buffer
    glLoadIdentity();                   # Reset The View
    glTranslatef(0,-0.50,-6.0)             # Move Left And Into The Screen
    glScalef(1.2,1.2,1.2)
    glRotatef(-75,1.0,0.0,0.0)
    glRotatef(rtri,0.0,0.0,1.0)
    #glutSolidSphere(2,20,20) 
    #Rotate The Pyramid On It's Y Axis
    glColor3f(1,0,0)
  
    
    for k in vv:
        if k.id==sh_data[0]:
             k.type_render=1
             glTranslatef(0,0,0)
             k.render()
             glTranslatef(0,0,0)
        else:
            k.type_render=0
        k.render()

  
    

    rtri  = rtri +1.5                  # Increase The Rotation  
    
    #  since this is double buffered, swap the buffers to display what just got drawn. 
    glutSwapBuffers()

    
def InitGL(Width, Height):              # We call this right after our OpenGL window is created.
    glClearColor(0.3, 0.3, 0.9, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
    glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
    glEnable(GL_LIGHTING)
    #glDisable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glEnable( GL_COLOR_MATERIAL ) ;
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0,+2,1 ) )
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1,1,1) )
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.47,0.47,0.47) )
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.01)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                     # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)     # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
                           
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        glutDestroyWindow(window)
        sys.exit()
    nd= ord(args[0])   
    if nd==50:
       sh_data[0]+=1
       
    if nd==51:
       sh_data[0]-=1
       
    sh_data[0]=max(sh_data[0],0)
    sh_data[0]=min(len(vv)-1, sh_data[0] )
    print "OBJ ID:",sh_data[0]
    print "Name:",toname(vv[sh_data[0] ].name) , vv[sh_data[0] ].mat_id
        
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
        glutInit(sys.argv)
         
                              
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(0, 0)
        window = glutCreateWindow("VOB View")   
        glutDisplayFunc(DrawGLScene)
        glutIdleFunc(DrawGLScene)       

        glutReshapeFunc(ReSizeGLScene)
    
    

        glutKeyboardFunc(keyPressed)
    

        InitGL(640, 480)
main()
glutMainLoop()
        
sys.exit(0) 

