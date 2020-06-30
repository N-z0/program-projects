#!/usr/bin/env python3
# noqa: E402
import gi 
gi.require_version('Gtk', '3.0')
import numpy as np
from gi.repository import Gtk, Gdk

### OpenGL
from OpenGL.GLU import *
from OpenGL import GL
#from OpenGL.GLUT import *
#rom OpenGL.GLE import *
#from OpenGL.GL.ARB.multitexture import *
from OpenGL.GL import shaders
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays,glBindVertexArray

#----------------------------------------------------------------------

VERTEX_SHADER = """
    #version 330
    in vec4 position;
    void main()
    {
        gl_Position = position;
    }"""

FRAGMENT_SHADER = """
    #version 330
    out vec4 fragColor;
    void main()
    {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
    """



class GLWarper():
    def __init__(self,gl_canva):
        self.gl_canva = gl_canva

        # Sets the version of OpenGL required by this OpenGL program
        gl_canva.set_required_version(3, 3)
        self.test_features(gl_canva)

        gl_canva.set_has_depth_buffer(True)
        gl_canva.set_has_stencil_buffer(False)
        gl_canva.set_double_buffered(False)
        
        #gl_canva.connect('create-context', self.on_context)
        gl_canva.connect('realize', self.on_initialize)
        #gl_canva.connect('resize', self.on_resize)
        gl_canva.connect('render', self.on_render)
        #gl_canva.connect('unrealize', self.on_uninitialize)

        self.vertices = [
            0.6,  0.6, 0.0, 1.0,
            -0.6,  0.6, 0.0, 1.0,
            0.0, -0.6, 0.0, 1.0]
        self.vertices = np.array(self.vertices, dtype=np.float32)
        


    def test_features(self,gl_canva):
        print('Testing features')
        print('glGenVertexArrays Available %s' % bool(glGenVertexArrays))
        print('Alpha Available %s' % bool(gl_canva.get_has_alpha()))
        print('Depth buffer Available %s' % bool(gl_canva.get_has_depth_buffer()))


    def on_context(self, gl_area):
        # not needed except for special instances, read the docs
        c = gl_area.get_context()
        print("ON_CONTEXT")
        return c



    def on_initialize(self, widget):
        print("ON_REALIZE")

        widget.make_current()
        # Checks to see if there were errors creating the context
        if widget.get_error() != None:
            print(widget.get_error())

        vs = shaders.compileShader(VERTEX_SHADER, GL.GL_VERTEX_SHADER)
        fs = shaders.compileShader(FRAGMENT_SHADER, GL.GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vs, fs)

        # Create a new Vertex Array Object
        self.vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vertex_array_object )

        # Generate a new array buffers for our vertices
        self.vertex_buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertex_buffer)

        # Get position variable form the shader and store
        self.position = GL.glGetAttribLocation(self.shader, 'position')
        GL.glEnableVertexAttribArray(self.position)

        # describe the data layout
        GL.glVertexAttribPointer(self.position, 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))

        # Copy data to the buffer
        GL.glBufferData(GL.GL_ARRAY_BUFFER, 48, self.vertices, GL.GL_STATIC_DRAW)

        # Unbind buffers once done
        GL.glBindVertexArray( 0 )
        GL.glDisableVertexAttribArray(self.position)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        return True


    def on_uninitialize(self, gl_area):
        print("ON_UNREALIZE")

    def on_render(self, widget, *args):
        print("ON_RENDER")
        # Checks to see if there were errors creating the context
        if widget.get_error() != None:
            print(widget.get_error())

        # clear screen and select shader for drawing
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glUseProgram(self.shader)

        # bind and draw vertices
        GL.glBindVertexArray(self.vertex_array_object)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        GL.glBindVertexArray(0)

        GL.glUseProgram(0)
        GL.glFlush()
        return True

    def on_resize(self,gl_area,width,height):
        print("ON_RESIZE")



