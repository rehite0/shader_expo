#!/usr/bin/env python
import subprocess as sp
from dataclasses import dataclass
from time import sleep
import numpy as np
import pygame as pg
import ctypes
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from utils import *

@dataclass
class preview:
    vao=None
    vbo=None
    pid=None
    vs="shaders/vert.vs.glsl"
    fs="shaders/frag.fs.glsl"
    vert=full_square
    vnum=None
    '''
    def __init__(self,tvs=None,tfs=None,tvert=None):
        self.vs=tvs or self.vs
        self.fs=tfs or self.fs
        self.vert=tvert or self.vert'''
@dataclass 
class uniform:
    frameno=0
    framerate=0.0
    time=0.0
    dtime=0.0
    mcoord=(0.0,0.0)
    resolution=(0.0,0.0)


def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
    with open(vertex_filepath,'r') as f:
        vertex_src = f.readlines()

    with open(fragment_filepath,'r') as f:
        fragment_src = f.readlines()
    
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
    return shader

def load_buffer(dis):
    dis.vnum = len(dis.vert)//6
    dis.vert = np.array(dis.vert, dtype=np.float32)


    dis.vao=glGenVertexArrays(1) 
    glBindVertexArray(dis.vao)
    dis.vbo=glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, dis.vbo)
    glBufferData(GL_ARRAY_BUFFER, dis.vert.nbytes, dis.vert, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

def update_uniforms(uni,uid):

	glUniform1i(uid[0],	uni.frameno)
	glUniform1f(uid[1],	uni.framerate)
	glUniform1f(uid[2],	uni.time)
	glUniform1f(uid[3],	uni.dtime)
	glUniform2f(uid[4],	uni.mcoord[0],	uni.mcoord[1])
	glUniform2f(uid[5],	uni.resolution[0],	uni.resolution[1])

def main():
    clock=None
    uni=uniform()
    dis=preview()
    try:
        pg.init()
        pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)
        clock = pg.time.Clock()

        glClearColor(0.1, 0.2, 0.2, 1)
        
        load_buffer(dis)
        dis.pid=create_shader(
            vertex_filepath = dis.vs, 
            fragment_filepath = dis.fs)

        uid=[
            glGetUniformLocation(dis.pid,"frameno")
        	,glGetUniformLocation(dis.pid,"framerate")
        	,glGetUniformLocation(dis.pid,"time")
        	,glGetUniformLocation(dis.pid,"dtime")
        	,glGetUniformLocation(dis.pid,"mcoord")
        	,glGetUniformLocation(dis.pid,"resolution")
        ]

        running = True
        while (running):
            uni.frameno+=1
            if uni.frameno%40==0:
                glDeleteProgram(dis.pid)
                dis.pid=create_shader(
                    vertex_filepath = dis.vs, 
                    fragment_filepath = dis.fs)

            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(dis.pid)
            glBindVertexArray(dis.vao)
            
            update_uniforms(uni, uid)
            glDrawArrays(GL_TRIANGLES, 0, dis.vnum)


            pg.display.flip()

            #timing
            clock.tick(60)
    finally:
        glDeleteVertexArrays(1,(dis.vao,))
        glDeleteBuffers(1,(dis.vbo,))

        glDeleteProgram(dis.pid)
        pg.quit()

        
if __name__ == "__main__":
    main()
