#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_cam;

out vec3 normal;
out vec2 uv;
out vec3 pos;

void main() {
  mat4 mv = m_cam * m_model; 
  vec4 p = mv * vec4(in_position, 1.0);
  gl_Position = m_proj * p;
  // mat3 m_normal = transpose(inverse(mat3(mv)));
  // normal = m_normal * in_normal;
  normal = in_normal;
  uv = in_texcoord_0;
  pos = p.xyz;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
uniform mat4 m_proj;

in vec3 normal;
in vec3 pos;
in vec2 uv;

const vec4 light_dir = normalize(vec4(0.0, 1.0, 0.5, 0.0));
const vec4 light_col = vec4(1.0, 0.0, 0.0, 1.0);
const vec4 ambient_col = vec4(0.0, 0.0, 1.0, 1.0);

void main() {
  float l = dot(normalize(light_dir * m_proj), normalize(vec4(normal, 0.0)));
  vec4 color = texture(texture0, uv);
  fragColor = color * ambient_col * 0.25 + color * light_col * 0.75  * max(0.0, l);
}

#endif
