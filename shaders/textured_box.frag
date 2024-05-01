# version 330

in vec3 color;

out vec4 fragColor;

uniform sampler2D symbol;

void main() {
    fragColor = vec4 (color, 1);

}