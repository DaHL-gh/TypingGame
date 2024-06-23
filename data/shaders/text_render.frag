# version 330

in vec2 uv;
in vec3 color;

out vec4 fragColor;

uniform sampler2D symbol;

void main() {
    float opacity = texture(symbol, uv).x;

//    float A = 4., s = 1./A, x, y;
//
//    for (x=-.5; x<.5; x+=s) for (y=-.5; y<.5; y+=s) opacity += texture(symbol, uv + vec2(x * 0.05, y * 0.05)).x * (1 - x + y);
//
//	opacity *= s*s;

    fragColor = vec4 (color, opacity);
}