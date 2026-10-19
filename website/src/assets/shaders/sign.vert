varying vec2 vTexcoord;
varying vec3 vNormal;
varying vec3 vWorldPosition;

void main()
{
    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    vWorldPosition = worldPosition.xyz;

    vec4 worldNormal = modelMatrix * vec4(normal, 0.0);
    vNormal = worldNormal.xyz;

    vTexcoord = uv;

    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
