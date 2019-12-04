#version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_offset;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 v_texture;

void main() {
    gl_Position = projection * view * model * vec4(a_position + a_offset, 1.0);
    v_texture = a_texture;
}
