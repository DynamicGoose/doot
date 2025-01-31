#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;
in vec3 in_color0;
in vec3 position;

uniform mat4 m_proj;
uniform mat4 m_model;
uniform mat4 m_cam;
uniform mat4 m_mv;

out vec3 color;
out vec2 uv;
out vec3 pos;
out vec3 normal;
out mat4 mv;

void main() {
  // mv = m_cam * m_model;
  mv = m_mv;
  vec4 p = m_cam * m_model * vec4(in_position, 1.0);
  gl_Position = m_proj * p;
  mat3 m_normal = transpose(inverse(mat3(mv)));
  normal = m_normal * in_normal;
  pos = p.xyz;
  color = in_color0;
  uv = in_texcoord_0;
}

#elif defined FRAGMENT_SHADER

in mat4 mv;
in vec3 color;
in vec2 uv;
in vec3 pos;
in vec3 normal;

out vec4 fragColor;

void main(void){
  // calculate light diffusion
  vec4 light_pos = vec4(0.0, 0.0, 11.0, 1.0);
  vec3 light_col = vec3(1.0, 1.0, 1.0);
  float ambient_strength = 0.2;
  float specular_strength = 0.5;
  
  vec3 light = normalize(mv * light_pos - vec4(pos, 1.0)).xyz; 
  vec3 view = normalize(-pos); 
  vec3 normal = normalize(normal);

  // calculate ambience
  vec4 ambient = vec4(ambient_strength * light_col, 1.0);

  // get vector to light
  vec4 diff = vec4(max(dot(normal, light), 0.0) * light_col, 1.0);
  vec4 diffuse = clamp(diff, 0.0, 1.0);

  // Blinn specular variation
  vec3 halfDir = normalize(light + view);
  float spec = pow(max(dot(normal, halfDir), 0.0), 32);
  vec4 specular = clamp(vec4(specular_strength * spec * light_col, 1.0), 0.0, 1.0);

  // do calculations on every fragment
  fragColor = (ambient + diffuse + specular) * vec4(color, 1.0);
}

#endif
