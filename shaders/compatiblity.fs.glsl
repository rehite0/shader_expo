#version 430

uniform int	frameno;
uniform float	framerate;
uniform float	time;
uniform float	dtime;
uniform vec2	mcoord;
uniform vec2	resolution;
in vec3	fragmentColor;

out vec4 color;

vec3      iResolution=vec3(resolution.xy,0.0);// viewport resolution (in pixels)
float     iTime=time;                	 // shader playback time (in seconds)
float     iTimeDelta=dtime;              // render time (in seconds)
float     iFrameRate=framerate;          // shader frame rate
int       iFrame=frameno;		 // shader playback frame
vec4      iMouse=vec4(mcoord.xy,0.0,0.0);// mouse pixel coords. xy: current (if MLB down), zw: click

//shadertoy code goes here---->

//shadertoy code ends here --------------------------

void main()
{
    mainImage( color, gl_FragCoord.xy); 
}
