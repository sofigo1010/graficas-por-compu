
from xml.dom.expatbuilder import FragmentBuilder

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    outPosition = modelMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals; // Ajuste de normales para iluminación correcta
}
'''
fragment_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(normalize(outNormals), lightDir), 0.0); // Asegura que no haya valores negativos
    vec4 texColor = texture(tex, outTexCoords);
    fragColor = texColor * intensity;
}
'''
fat_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec3 pointLight;

void main()
{
    outPosition = modelMatrix * vec4(position + normals * sin(time * 3) / 10, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}
'''
water_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec3 pointLight;

void main()
{
    outPosition = modelMatrix * vec4(position + vec3(0, 1, 0) * sin(time * position.x * 10) / 10, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}
'''
negative_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(normalize(outNormals), lightDir), 0.0);
    vec4 texColor = texture(tex, outTexCoords);
    fragColor = 1 - (texColor * intensity); // Invertir el color en áreas iluminadas
}
'''



## nuevos


explosion_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform float explosionIntensity;
uniform vec3 explosionCenter;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float pulse = sin(time * 3.0) * explosionIntensity;
    vec3 toVertex = position - explosionCenter;
    vec3 explosionDisplacement = normalize(toVertex) * pulse;
    explosionDisplacement += normals * sin(dot(position, vec3(10.0)) * pulse) * 0.1;
    vec3 explodedPosition = position + explosionDisplacement;
    outPosition = modelMatrix * vec4(explodedPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}
'''
curve_vshader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vec3 offset = normalize(position) * sin(time + length(position) * 10.0) * 0.2;
    vec3 fragmentedPosition = position + offset;
    outPosition = modelMatrix * vec4(fragmentedPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}
'''
spiral_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float distance = length(position.xy);
    float angle = atan(position.y, position.x) + time * 10.0;

    float radius = sin(time * 3.0) * 1.0 + 1.0;
    float spiralStrength = exp(-distance * 2.0);

    vec3 spiralOffset = vec3(cos(angle) * distance * spiralStrength * radius * 2.0, 
                             sin(angle) * distance * spiralStrength * radius * 2.0, 
                             0.0);

    vec3 whirlpoolPosition = position - spiralOffset;

    outPosition = modelMatrix * vec4(whirlpoolPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}
'''
star_expand_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

out vec2 outTexCoords;
out vec3 outNormals;
out vec4 outPosition;

uniform float time;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    float distance = length(position.xy);
    float angle = atan(position.y, position.x);

    float starEffect = abs(sin(angle * 8.0)) * 0.7;
    float pulse = sin(time * 3.0) * 0.5 + 0.5;
    float expand = starEffect * pulse * 0.5;

    vec3 starPosition = position + normalize(position) * expand;

    outPosition = modelMatrix * vec4(starPosition, 1.0);
    gl_Position = projectionMatrix * viewMatrix * outPosition;
    outTexCoords = texCoords;
    outNormals = mat3(transpose(inverse(modelMatrix))) * normals;
}
'''
aura_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;
uniform float time;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(normalize(outNormals), lightDir), 0.0);

    vec4 texColor = texture(tex, outTexCoords);

    float auraIntensity = pow(1.0 - intensity, 4.0);
    vec3 auraColor = vec3(1.0, 1.0, 0.0) * auraIntensity * 1.5;

    float pulse = sin(time * 3.0) * 0.5 + 0.5;
    vec3 expandedColor = mix(texColor.rgb, vec3(1.0, 0.0, 0.0), pulse);

    vec3 finalColor = expandedColor + auraColor;

    fragColor = vec4(finalColor, texColor.a);
}
'''
electric_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;
uniform float time;

out vec4 fragColor;

void main()
{
    vec3 lightDir = normalize(pointLight - outPosition.xyz);
    float intensity = max(dot(normalize(outNormals), lightDir), 0.0);

    vec4 texColor = texture(tex, outTexCoords);

    float lightningPattern = fract(sin(dot(outPosition.xy * 30.0, vec2(12.9898, 78.233))) * 43758.5453);
    float lightning = step(0.95, abs(sin(outPosition.x * 15.0 + time * 40.0) * lightningPattern * 2.0));

    float boltShape = abs(sin(outPosition.y * 30.0 + time * 20.0));
    float finalLightning = step(0.8, boltShape) * lightning;

    vec3 lightningColor = mix(vec3(0.2, 0.4, 1.0), vec3(1.0, 1.0, 1.0), finalLightning * 2.0);

    vec3 finalColor = mix(texColor.rgb, lightningColor, finalLightning);

    fragColor = vec4(finalColor * intensity, texColor.a);
}
'''
disintegration_shader = '''
#version 450 core

in vec2 outTexCoords;
in vec3 outNormals;
in vec4 outPosition;

uniform sampler2D tex;
uniform vec3 pointLight;
uniform float time;

out vec4 fragColor;

void main()
{
    vec4 texColor = texture(tex, outTexCoords);
    float noise = fract(sin(dot(outPosition.xy, vec2(12.9898, 78.233))) * 43758.5453 + time * 5.0);
    float dissolve = smoothstep(0.3, 0.7, noise);

    vec3 startColor = vec3(0.0, 0.0, 1.0);
    vec3 endColor = vec3(0.5, 0.0, 1.0);
    vec3 disintegrationColor = mix(startColor, endColor, dissolve);

    float sparkEffect = step(0.9, abs(sin(time * 20.0 + noise * 10.0)));
    disintegrationColor += vec3(1.0, 1.0, 1.0) * sparkEffect * 0.3;

    vec3 finalColor = mix(texColor.rgb, disintegrationColor, dissolve);

    if (dissolve < 0.5) {
        discard;
    }

    fragColor = vec4(finalColor, texColor.a);
}
'''