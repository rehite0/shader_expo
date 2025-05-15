#!/usr/bin/env bash

#mv ./shader/frag.fs.glsl 
./main.py &
cat ./shaders/def.fs.glsl > ./shaders/frag.fs.glsl
nvim ./shaders/frag.fs.glsl
