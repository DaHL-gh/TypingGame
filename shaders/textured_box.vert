# version 330

in vec2 in_position;
in vec3 in_color;
in vec2 texture_cords;

out vec3 color;
out vec2 uv;

void main() {
    color = in_color;
    uv = texture_cords;
    gl_Position = vec4(in_position, 0, 1);
}