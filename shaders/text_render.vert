# version 330

in vec2 in_position;
in vec2 in_bitmap_cords;
in vec3 in_color;

out vec2 uv;
out vec3 color;

uniform vec2 w_pos;

void main() {
    uv = in_bitmap_cords;
    color = in_color;

    vec2 screen_pos = vec2 (w_pos.x + 1, w_pos.y) + vec2 (in_position.x, in_position.y - 1);
    gl_Position = vec4 (screen_pos, 0, 1);
}