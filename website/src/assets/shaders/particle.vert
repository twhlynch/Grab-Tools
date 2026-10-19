attribute vec3 color;
attribute float scale;

varying vec3 vColor;
varying vec3 vWorldPosition;

void main()
{
    vColor = color;

    vec4 worldPosition = modelMatrix * vec4(position, 1.0);
    vWorldPosition = worldPosition.xyz;

    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = scale * (300.0 / length(mvPosition.xyz));
    gl_Position = projectionMatrix * mvPosition;
}
