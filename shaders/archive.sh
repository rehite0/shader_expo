#!/usr/bin/env bash

a=$1
test -n "$a" ||echo 'enter file name:' && read a
echo "are you sure you want to copy $a.fs.glsl to frag.fs.glsl?"
read 
cat frag.fs.glsl >"./archive/$a.fs.glsl"
