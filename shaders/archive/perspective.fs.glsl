#version 430

uniform int	frameno;
uniform float	framerate;
uniform float	time;
uniform float	dtime;
uniform vec2	mcoord;
uniform vec2	resolution;
in vec3	fragmentColor;

out vec4 color;

vec3 draw_point( vec3 cam, vec3 camd, vec3 p, float r){
    //calculate distance between ray and point
    //float dist=length(cross(p-cam,camd))/length(camd);
    //or 
    float dist=length(p-cam-dot(p-cam,camd)*camd);
    return  vec3(smoothstep(r,r+0.01,dist));
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
    float rad=0.1;

    // pixel color
    vec3 col =draw_point(cam,camd,p,rad);

    // Output to screen
    color = vec4(col,1.0);
}
