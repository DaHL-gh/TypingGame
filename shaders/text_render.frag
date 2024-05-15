# version 330

in vec2 uv;

out vec4 fragColor;

uniform sampler2D symbol;

void main() {
    float opacity = texture(symbol, uv).x;

    fragColor = vec4 (vec3 (1), opacity);
}