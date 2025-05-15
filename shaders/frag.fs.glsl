#version 430

uniform int		frameno
uniform float	framerate
uniform float	time
uniform float	dtime
uniform vec2	mcoord
uniform vec2	resolution
in vec3	fragmentColor;

out vec4 color;

void main()
{
    color = vec4(fragmentColor, 1.0);
}
