#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 mvp;
uniform mat4 m_model;

void main() {
    gl_Position = mvp * m_model * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

// out vec4 outColor;

void main() {
    // outColor = vec4(1.0);
}

#endif
