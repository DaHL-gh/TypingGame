# version 330

in vec2 uv;
in vec3 color;

out vec4 fragColor;

uniform sampler2D symbol;

void main() {
    float opacity = texture(symbol, uv).x;

    fragColor = vec4 (color, opacity);
}