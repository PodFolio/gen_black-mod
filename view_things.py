import struct
import math
import Image
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


import blackwood


global textures_gl
textures_gl={}

global tex_idd

global glists
glists={}
tex_idd={}

def next_p2 (num):
	""" If num isn't a power of 2, will return the next higher power of two """
	rval = 1
	while (rval<num):
		rval <<= 1
	return rval

    
def render_obj(name ):
    global s
    global glists
    global tex_idd
    DEFAULT="FBM_BMW"
    if  tex_idd.has_key( name ):
      tex_name=  tex_idd[name]
    else:
        tex_idd[name] =     s.get_obj_file_texture(name)
        tex_name=  tex_idd[name]    
    #tex_name = s.get_obj_file_texture(name)
    if tex_name == "DEFAULT":
        tex_name= DEFAULT
    
    if textures_gl.has_key(tex_name):
       if textures_gl[tex_name]  ==None:
           glDisable(GL_TEXTURE_2D);
       else:    
         glEnable(GL_TEXTURE_2D);            
         glBindTexture(GL_TEXTURE_2D, textures_gl[tex_name] )
         
 
    else:
        print "TEX BUILD"
        tbase= "D:\\Documents and Settings\\DrRafael\\Desktop\\scripts\\veh"
        
        status,tid= BuildTexture( os.path.join( tbase,  tex_name  +".jpg") )
        if status==False:
           print "ERROR ! TEXTURRE NOT FOUND:",  tex_name +".jpg"  
           textures_gl[tex_name] = None
        else:
            textures_gl[tex_name]  = tid

    if glists.has_key(name) :
       glBegin(GL_TRIANGLES) 
       glCallList( glists[name] )
       
       glEnd()
    else:
       glists[name] =   glGenLists(1)
       glNewList(glists[name] , GL_COMPILE)
       #print "BUILD ", name
       for m in [0,1,2,3,4,5,6,7,8]:       
             xyzuv = s.get_xyzuf_list( name,m  )
             for p in xyzuv :
                glTexCoord2f( p[3], 1.0 - p[4] ) 
                glVertex3f(p[0],p[1],p[2])
             for p in xyzuv :
                glTexCoord2f( p[3], 1.0 - p[4] ) 
                glVertex3f(-p[0],p[1],p[2])
                
       glEndList()

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







def DrawGLScene():     
    global rtri
    global obj
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); # Clear The Screen And The Depth Buffer
    glLoadIdentity();                   # Reset The View
    glTranslatef(0,-0.50,-6.0)             # Move Left And Into The Screen
    glScalef(1.2,1.2,1.2)
    glRotatef(-75,1.0,0.0,0.0)
    glRotatef(rtri,0.0,0.0,1.0)
    glColor3f(1,1,1)
  
    
    for k in obj :
         render_obj(k)

    rtri  = rtri +1.5                  # Increase The Rotation      
    #  since this is double buffered, swap the buffers to display what just got drawn. 
    glutSwapBuffers()

    


def InitGL(Width, Height):              # We call this right after our OpenGL window is created.
    glClearColor(0.3, 0.3, 0.9, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
    #glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
    #glEnable(GL_LIGHTING)
    #glDisable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glColor3f(1,1,1)
    #glEnable( GL_COLOR_MATERIAL ) ;
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0,+2,1 ) )
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1,1,1) )
    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.47,0.47,0.47) )
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.01)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
ESCAPE = '\033'    
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == ESCAPE:
        glutDestroyWindow(window)
        sys.exit()

def ReSizeGLScene(Width, Height):
    if Height == 0:                     # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)     # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
 

 
        global s
        global rtri
        global obj
        
        ff=[]

        rtri =0
        
        s= blackwood.blk_file()
        name = "veh\\Blackwood.wld"
        s.load(name)
        s.set_mid(40) 
        obj= s.get_obj_names()

  
        glutInit(sys.argv)
         
                              
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(0, 0)
        window = glutCreateWindow("View things")   
        glutDisplayFunc(DrawGLScene)
        glutIdleFunc(DrawGLScene)       

        glutReshapeFunc(ReSizeGLScene)
    
    

        glutKeyboardFunc(keyPressed)
    

        InitGL(640, 480)

main()
glutMainLoop()
        
sys.exit(0) 
