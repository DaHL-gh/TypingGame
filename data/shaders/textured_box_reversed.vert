# version 330

in vec2 in_position;
in vec2 in_texture_cords;

out vec2 uv;

void main() {
    uv = in_texture_cords;
    gl_Position = vec4(in_position, 0, 1);
    gl_Position.y = -gl_Position.y;
}