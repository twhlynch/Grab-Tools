varying vec3 vWorldPosition;

uniform vec3 cameraFogColor0;
uniform vec3 cameraFogColor1;
uniform float sunSize;

uniform vec3 sunColor;
uniform vec3 sunDirection;

void main()
{
    vec3 cameraToVertex = normalize(vWorldPosition);

    float horizonFactor = 1.0 - clamp(abs(cameraToVertex.y) / 0.8, 0.0, 1.0);
    vec3 fogColor = mix(cameraFogColor1.rgb, cameraFogColor0.rgb, horizonFactor * horizonFactor);
    vec4 color = vec4(fogColor, 1.0);

    float sunAngle = acos(dot(sunDirection, -cameraToVertex));
    float realSunSize = 0.05 * sunSize;
    float sunGlowSize = sunSize;
    float sunFactor = clamp((sunGlowSize - sunAngle) / sunGlowSize, 0.0, 1.0);
    sunFactor *= sunFactor;
    if (sunAngle < realSunSize) sunFactor = 1.5;
    color.rgb = mix(color.rgb, sunColor, sunFactor);

    gl_FragColor = color;
    #include <colorspace_fragment>
}
