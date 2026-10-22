varying vec3 vWorldPosition;

void main()
{
    vec3 rotatedPosition = (modelViewMatrix * vec4(position, 0.0)).xyz;
    gl_Position = projectionMatrix * vec4(rotatedPosition, 0.0);
    gl_Position.z = gl_Position.w;

    vWorldPosition = position;
}
