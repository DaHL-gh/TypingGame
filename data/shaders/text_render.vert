# version 330

in vec2 in_position;
in vec2 in_texture_cords;
in vec3 in_color;

out vec2 uv;
out vec3 color;

void main() {
    uv = in_texture_cords;
    color = in_color;

    gl_Position = vec4 (in_position, 0, 1);
}