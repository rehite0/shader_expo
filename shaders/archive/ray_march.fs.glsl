#version 430

uniform int	frameno;
uniform float	framerate;
uniform float	time;
uniform float	dtime;
uniform vec2	mcoord;
uniform vec2	resolution;
in vec3	fragmentColor;

out vec4 color;

float sdSphere( vec3 p, float s )
{
  return length(p)-s;
}
vec3 md_spher(vec3 cam, vec3 camd, vec3 p, float r){
    vec3 t=cam;
    float dio=0.0;
    for(int i=0;i<100;i++){
	float dist=sdSphere(p-t,r);
	dio+=dist;
	if (dist<=0.005)
	    return vec3(vec3((length(p-cam)-dio)/r).xy,0.0);
	else
	    t+=dist*camd;
    }
    return vec3(0.);//mindis;
}
void main()
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = gl_FragCoord.xy/resolution;

    uv=uv*2.0-1.0;
    //coord of camera
    vec3 cam=vec3(0.0,0.0,2.0);
    //vector from camera to every pixel's uv coord
    vec3 camd=normalize(vec3(uv.xy,0.0)-cam);

    //coord of point
    vec3 p=vec3(0.7*sin(time),0.7*sin(time),0.7*cos(time));
    float rad=0.15;

    // pixel color
    vec3 col =md_spher(cam,camd,p,rad);

    // Output to screen
    color = vec4(col,1.0);
}
