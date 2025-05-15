#version 430

uniform int	frameno;
uniform float	framerate;
uniform float	time;
uniform float	dtime;
uniform vec2	mcoord;
uniform vec2	resolution;
in vec3	fragmentColor;

out vec4 color;

void main()
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = gl_FragCoord.xy/resolution;

    // Time varying pixel color
    vec3 col = 0.5 + 0.5*cos(time+uv.xyx+vec3(0,2,4));

    // Output to screen
    color = vec4(col,1.0);
}
