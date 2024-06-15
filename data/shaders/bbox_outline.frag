# version 330

in vec2 uv;

out vec4 fragColor;

uniform sampler2D in_texture;
uniform vec2 w_size;

void main() {
    float opacity = 0.3;
    vec3 color = texture(in_texture, uv).xyz;

    opacity += step(uv.x, 1 / w_size.x);
    opacity += step(uv.y, 1 / w_size.y);

    opacity += step(1 - uv.x, 1 / w_size.x);
    opacity += step(1 - uv.y, 1 / w_size.y);

    color.x += opacity;
    fragColor = vec4 (color, opacity);
}