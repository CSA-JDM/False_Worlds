#version 330

in layout(location = 0) vec3 a_position;
in layout(location = 1) vec2 a_texture;
in layout(location = 2) vec3 a_offset;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 v_texture;

void main() {
    gl_Position = projection * view * model * vec4(a_position + a_offset, 1.0);
    v_texture = a_texture;
}
