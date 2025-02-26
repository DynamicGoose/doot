#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

uniform mat4 m_model;
uniform mat4 m_camera;
uniform mat4 m_proj;
uniform mat4 mvp;

out vec3 fragPos;
out vec3 normal;
out vec4 fragPosLightSpace;
out vec2 uv;

void main() {
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = transpose(inverse(mat3(m_model))) * in_normal;
    uv = in_texcoord_0;
    fragPosLightSpace = mvp * vec4(fragPos, 1.0);
    gl_Position = m_proj * m_camera * vec4(fragPos, 1.0);
}

#elif defined FRAGMENT_SHADER

in vec3 fragPos;
in vec3 normal;
in vec4 fragPosLightSpace;
in vec2 uv;

uniform sampler2D shadowMap;
uniform sampler2D texture1;
uniform vec3 lightPos;
uniform vec3 viewPos;

out vec4 fragColor;

float ShadowCalculation(vec4 fragPosLightSpace, float bias) {
    // perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    // get closest depth value from light's perspective (using [0,1] range fragPosLight as coords)
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    // get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    // check whether current frag pos is in shadow
    float shadow = currentDepth - bias > closestDepth ? 1.0 : 0.0;

    return shadow;
}

void main() {
    vec3 color = texture(texture1, uv).rgb;
    vec3 normal = normalize(normal);
    vec3 lightColor = vec3(1.0);
    // ambient
    vec3 ambient = 0.15 * lightColor;
    // diffuse
    vec3 lightDir = normalize(lightPos - fragPos);
    float diff = max(dot(lightDir, normal), 0.0);
    vec3 diffuse = diff * lightColor;
    // specular
    vec3 viewDir = normalize(viewPos - fragPos);
    float spec = 0.0;
    vec3 halfwayDir = normalize(lightDir + viewDir);
    spec = pow(max(dot(normal, halfwayDir), 0.0), 64.0);
    vec3 specular = spec * lightColor;
    // calculate shadow
    float bias = max(0.005 * (1.0 - dot(normal, lightDir)), 0.0005);
    float shadow = ShadowCalculation(fragPosLightSpace, bias);
    vec3 lighting = (ambient + (1.0 - shadow) * (diffuse + specular)) * color;
    
    fragColor = vec4(lighting, 1.0);
}

#endif
