# version 330

in vec3 color;
in vec2 uv;

out vec4 fragColor;

uniform sampler2D symbol;

void main() {
    float opacity = texture(symbol, uv).x;
    vec3 color = vec3 (uv, 1);
    fragColor = vec4 (color, opacity);

}