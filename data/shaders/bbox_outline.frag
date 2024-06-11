# version 330

in vec2 uv;

out vec4 fragColor;

uniform vec2 w_size;

void main() {
    float opacity = 0;

    opacity += step(uv.x, 1 / w_size.x);
    opacity += step(uv.y, 1 / w_size.y);

    opacity += step(1 - uv.x, 1 / w_size.x);
    opacity += step(1 - uv.y, 1 / w_size.y);

    fragColor = vec4 (vec3 (1), opacity);
}