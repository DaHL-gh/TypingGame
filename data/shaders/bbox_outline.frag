# version 330

in vec2 uv;

out vec4 fragColor;

uniform vec2 w_size;

void main() {
    float opacity = 0.3;

    int width = 2;

    opacity += step(uv.x, width / w_size.x);
    opacity += step(uv.y, width / w_size.y);

    opacity += step(1 - uv.x, width / w_size.x);
    opacity += step(1 - uv.y, width / w_size.y);

    fragColor = vec4 (opacity);
}