#version 430

uniform int	frameno;
uniform float	framerate;
uniform float	time;
uniform float	dtime;
uniform vec2	mcoord;
uniform vec2	resolution;
in vec3	fragmentColor;

out vec4 color;

mat3 rotate_x(float a){float sa = sin(a); float ca = cos(a); return mat3(vec3(1.,.0,.0),    vec3(.0,ca,sa),   vec3(.0,-sa,ca));}
mat3 rotate_y(float a){float sa = sin(a); float ca = cos(a); return mat3(vec3(ca,.0,sa),    vec3(.0,1.,.0),   vec3(-sa,.0,ca));}
mat3 rotate_z(float a){float sa = sin(a); float ca = cos(a); return mat3(vec3(ca,sa,.0),    vec3(-sa,ca,.0),  vec3(.0,.0,1.));}

float sdTorus( vec3 p, vec2 t )
{
  p=rotate_x(3.14/2)*rotate_y(time)*rotate_z(time)*p;
  vec2 q = vec2(length(p.xz)-t.x,p.y);
  return length(q)-t.y;
}

float GetDist(vec3 p) {
    float r=0.4;
    float R=0.2;
    return sdTorus(p,vec2(r,R));
}
vec3 GetNormal(vec3 p) {
	float d = GetDist(p);
    vec2 e = vec2(.01, 0);
    
    vec3 n = d - vec3(
        GetDist(p-e.xyy),
        GetDist(p-e.yxy),
        GetDist(p-e.yyx));
    
    return normalize(n);
}

vec3 get_light(vec3 p){
    vec3 lightPos = vec3(2.0,0.0, 3.0);
    //lightPos.xz += vec2(sin(time), cos(time))*2.;
    vec3 l = normalize(lightPos-p);
    vec3 n = GetNormal(p);
    
    float dif = clamp(dot(n, l), 0., 1.);
    return vec3(dif);
}

vec3 md_torus(vec3 cam, vec3 camd, vec3 p){
    vec3 t=cam;
    float dio=0.0;
    for(int i=0;i<100;i++){
	float dist=GetDist(p-t);
	dio+=dist;
	if (dist<=0.005)
	    return get_light(p-t);
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
    vec3 cam=vec3(0.0,0.0,-2.0);
    //vector from camera to every pixel's uv coord
    vec3 camd=normalize(vec3(uv.xy,0.0)-cam);

    //coord of point
    vec3 p=vec3(0.);

    // pixel color
    vec3 col =md_torus(cam,camd,p);

    // Output to screen
    color = vec4(col,1.0);
}
