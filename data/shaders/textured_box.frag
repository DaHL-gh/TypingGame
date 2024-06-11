# version 330

in vec2 uv;

out vec4 fragColor;

uniform sampler2D in_texture;

void main() {
    fragColor = texture(in_texture, uv);
}