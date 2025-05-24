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
    clock=None
    
@dataclass 
class uniform:
    frameno=0
    framerate=0.0
    time=0.0
    dtime=0.0
    mcoord=(0.0,0.0)
    resolution=(0.0,0.0)


def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
    isbroken=0
    while (1):
        try:
            with open(vertex_filepath,'r') as f:
                vertex_src = f.readlines()

            with open(fragment_filepath,'r') as f:
                fragment_src = f.readlines()
            
            shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                    compileShader(fragment_src, GL_FRAGMENT_SHADER))
            if isbroken:
                print("reloaded!!")
            isbroken=0
            return shader
        except Exception as e:
            if str(e)!=isbroken:
                print(str(e).encode('latin-1').decode('unicode_escape'),"\n\n")
            isbroken=str(e)
            sleep(1.5)
            continue

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

def update_uniforms(uni,uid,dis):
    uni.coord=tuple(map(float,pg.mouse.get_pos()))
    uni.resolution=tuple(map(float,pg.display.get_window_size()))
    uni.frameno+=1
    uni.dtime=dis.clock.get_time()/1000
    uni.time+=uni.dtime
    uni.framerate=dis.clock.get_fps()
    glUniform1i(uid[0],	uni.frameno)
    glUniform1f(uid[1],	uni.framerate)
    glUniform1f(uid[2],	uni.time)
    glUniform1f(uid[3],	uni.dtime)
    glUniform2f(uid[4],	uni.mcoord[0],	uni.mcoord[1])
    glUniform2f(uid[5],	uni.resolution[0],	uni.resolution[1])

def main():
    dis=preview()
    uni=uniform()
    try:
        pg.init()
        pg.display.set_mode((640,480),pg.RESIZABLE, pg.OPENGL|pg.DOUBLEBUF)
        dis.clock = pg.time.Clock()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        
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

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        #glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        running = True
        while (running):
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
            
            update_uniforms(uni, uid, dis)
            glDrawArrays(GL_TRIANGLES, 0, dis.vnum)


            pg.display.flip()

            #timing
            dis.clock.tick(60)
    except Exception as e:
        raise e
    finally:
        glDeleteVertexArrays(1,(dis.vao,))
        glDeleteBuffers(1,(dis.vbo,))

        glDeleteProgram(dis.pid)
        pg.quit()

        
if __name__ == "__main__":
    main()
