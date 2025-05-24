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
void mainImage(out vec4 O, vec2 I)
{
    //Raymarch iterator, step distance and z-depth
    float i, d, z;
    //Clear fragColor and raymarch 100 steps
    for(O *= i; i++<1e2;
        //Pick color and glow
        O += (cos(z+vec4(6,1,2,3))+1.)/d)
    {
        //Raymarch sample point
        vec3 p = z * normalize(vec3(I+I,0)-iResolution.xyy);
        //Scroll forward
        p.z -= iTime;
        //Turbulence
        //https://mini.gmshaders.com/p/turbulence
        //Rounded for blocky effect
        for(d = .5; d < 3e1; d += d)
            p += cos((p*d)-z*.1).yzx/d;
        //Distance to depth columns
        z += d = length(sin(p.xy))*.1;
    }
    //Tanh tonemapping
    //https://www.shadertoy.com/view/ms3BD7
    O = tanh(O/5e3);
}
//shadertoy code ends here --------------------------

void main()
{
    mainImage( color, gl_FragCoord.xy); 
}
