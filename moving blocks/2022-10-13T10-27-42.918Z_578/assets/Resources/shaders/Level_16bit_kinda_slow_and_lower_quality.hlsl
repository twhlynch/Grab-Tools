//
//  Shaders.hlsl
//  Rayne
//
//  Copyright 2015 by Überpixel. All rights reserved.
//  Unauthorized use is punishable by torture, mutilation, and vivisection.
//

#ifndef RN_COLOR
#define RN_COLOR 0
#endif

#ifndef RN_USE_MULTIVIEW
#define RN_USE_MULTIVIEW 0
#endif

#ifndef COD_LAVA
#define COD_LAVA 0
#endif

#ifndef COD_ICE
#define COD_ICE 0
#endif

#ifndef COD_TRIPLANAR
#define COD_TRIPLANAR 0
#endif

#ifndef COD_STARTFINISH
#define COD_STARTFINISH 0
#endif

#ifndef COD_GRAPPLE_ROPE
#define COD_GRAPPLE_ROPE 0
#endif

#ifndef COD_UV0
#define COD_UV0 0
#endif

#ifndef COD_SHADOWS
#define COD_SHADOWS 0
#endif

#ifndef COD_FOG
#define COD_FOG 0
#endif

#ifndef COD_UNLIT
#define COD_UNLIT 0
#endif

#ifndef COD_SOFT_SHADOWS
#define COD_SOFT_SHADOWS 0
#endif

#if COD_TRIPLANAR || COD_UV0 || COD_GRAPPLE_ROPE
SamplerState linearRepeatSampler;
Texture2D texture0;
#endif

#if COD_SHADOWS
SamplerComparisonState directionalShadowSampler;
Texture2DArray directionalShadowTexture;
#endif

struct LightDirectional
{
	float4 direction;
	float4 color;
};

cbuffer vertexUniforms
{
#if RN_USE_MULTIVIEW
	matrix viewProjectionMatrix_multiview[2];
#else
	matrix viewProjectionMatrix;
#endif

#if COD_SHADOWS
	matrix directionalShadowMatrices[4];
#endif

#if COD_FOG || COD_SHADOWS || COD_ICE
	float3 cameraPosition;
#endif

#if COD_TRIPLANAR || COD_GRAPPLE_ROPE
	float textureTileFactor;
#endif
};

struct VertexInstanceUniformsData
{
	matrix modelMatrix;

#if !COD_UNLIT || COD_TRIPLANAR
	matrix normalMatrix;
#endif

	float4 ambientColor; //This is used for highlighting selected blocks in the editor, otherwise it usually has the same value for all blocks...
	float4 diffuseColor;
};

cbuffer vertexInstanceUniformsBuffer
{
	VertexInstanceUniformsData vertexInstanceUniforms[45]; //45 Should keep the uniform data within 8kb, which allows the quest hardware to access it much faster
};

cbuffer fragmentUniforms
{
	float4 cameraAmbientColor;

#if COD_FOG
	float4 cameraFogColor0;
	float4 cameraFogColor1;
	float2 cameraClipDistance;
	float2 cameraFogDistance;
#endif

#if !COD_UNLIT || COD_FOG
	#if COD_SHADOWS //&& COD_SOFT_SHADOWS
		float2 directionalShadowInfo;
	#endif
		LightDirectional directionalLights[1];
#endif

#if COD_TRIPLANAR && COD_LAVA
	float time;
#endif
};

struct InputVertex
{
	[[vk::location(0)]] float3 position : POSITION;
	uint instanceID : SV_InstanceID;

#if !COD_UNLIT || COD_TRIPLANAR
	[[vk::location(1)]] float3 normal : NORMAL;
#endif

#if RN_COLOR
	[[vk::location(3)]] float4 color : COLOR;
#endif

#if COD_UV0 || COD_GRAPPLE_ROPE
	[[vk::location(5)]] float2 texCoord0 : TEXCOORD0;
#endif

#if RN_USE_MULTIVIEW
	uint viewIndex : SV_VIEWID;
#endif
};

struct FragmentVertex
{
	float4 position : SV_POSITION;
#if !COD_UNLIT || COD_TRIPLANAR
	nointerpolation float3 worldNormal : NORMAL;
#endif

#if COD_FOG || COD_SHADOWS || COD_ICE
	float3 cameraToVertex : TEXCOORD3;
#endif

	float4 color : TEXCOORD1;
	float4 ambientColor : TEXCOORD2;

#if COD_TRIPLANAR
	float3 tiledWorldPositions : TEXCOORD0;
#endif

#if COD_STARTFINISH || COD_UV0 || COD_GRAPPLE_ROPE
	float2 texCoord0 : TEXCOORD0;
#endif

#if COD_SHADOWS
	float4 shadowPosition[4] : TEXCOORD4;
#endif
};


#if COD_SHADOWS
//basic 2x2 blur, with hardware bilinear filtering if enabled
half getShadowPCF2x2Blended(half4 projected, half4 projectedOther, half2 shadowInfo, half factor)
{
	half4 projectedFinal[4];
	projectedFinal[0] = projected;
	projectedFinal[1] = factor > 0.25h? projectedOther : projected;
	projectedFinal[2] = factor > 0.5h? projectedOther : projected;
	projectedFinal[3] = factor > 0.75h? projectedOther : projected;

	half shadow = directionalShadowTexture.SampleCmpLevelZero(directionalShadowSampler, projectedFinal[0].xyz, projectedFinal[0].w);
	shadow += directionalShadowTexture.SampleCmpLevelZero(directionalShadowSampler, half3(projectedFinal[1].xy + half2(shadowInfo.x, 0.0), projectedFinal[1].z), projectedFinal[1].w);
	shadow += directionalShadowTexture.SampleCmpLevelZero(directionalShadowSampler, half3(projectedFinal[2].xy + half2(0.0, shadowInfo.y), projectedFinal[2].z), projectedFinal[2].w);
	shadow += directionalShadowTexture.SampleCmpLevelZero(directionalShadowSampler, half3(projectedFinal[3].xy + half2(shadowInfo.x, shadowInfo.y), projectedFinal[3].z), projectedFinal[3].w);

	shadow *= 0.25;
	return shadow;
}
#endif

#if COD_SHADOWS
half getDirectionalShadowFactor(float4 shadowPosition[4], half camDistance)
{
	half3 startPositions = half3(2.5h, 12.0h, 60.0h);
	half3 zGreater = (startPositions < camDistance);
	half mapToUse = dot(zGreater, 1.0h);

	half4 projectedPosition = half4(shadowPosition[mapToUse].xyz / shadowPosition[mapToUse].w, mapToUse);
	projectedPosition.y *= -1.0h;
	projectedPosition.xy *= 0.5h;
	projectedPosition.xy += 0.5h;

	half mapToUseBlend = min(mapToUse + 1.0h, 3.0h);
	half4 projectedPositionBlend = half4(shadowPosition[mapToUseBlend].xyz / shadowPosition[mapToUseBlend].w, mapToUseBlend);
	projectedPositionBlend.y *= -1.0h;
	projectedPositionBlend.xy *= 0.5h;
	projectedPositionBlend.xy += 0.5h;

	half2 fadeDistances[4];
	fadeDistances[0] = half2(2.0h, 0.5h);
	fadeDistances[1] = half2(10.0h, 2.0h);
	fadeDistances[2] = half2(55.0h, 5.0h);
	fadeDistances[3] = half2(60.0h, 1.0h);
	half factor = (camDistance - fadeDistances[projectedPosition.w].x) / fadeDistances[projectedPosition.w].y;

//#if COD_SOFT_SHADOWS
//	return getShadowPCF2x2Blended(projectedPosition.xywz, projectedPositionBlend.xywz, directionalShadowInfo, factor);
//#else
	half shadowNear = directionalShadowTexture.SampleCmpLevelZero(directionalShadowSampler, projectedPosition.xyw, projectedPosition.z);
	half shadowFar = directionalShadowTexture.SampleCmpLevelZero(directionalShadowSampler, projectedPositionBlend.xyw, projectedPositionBlend.z);
	return lerp(shadowNear, shadowFar, saturate(factor));
//#endif
}
#endif

#if !COD_UNLIT
half3 getDirectionalLights(half3 lightDirection, half4 lightColor, half3 normal
#if COD_SHADOWS
	, float4 shadowPosition[4], half camDistance
#endif
)
{
	half light = dot(normal, -lightDirection);
	half finalLight = saturate(light);
#if COD_SHADOWS
	finalLight *= getDirectionalShadowFactor(shadowPosition, camDistance);
#endif
#if COD_LAVA
	finalLight *= 0.5h;
#endif
	finalLight -= saturate(-light * 0.15h);
	return lightColor.rgb * finalLight * saturate(lightColor.a * 0.7h + 0.3h);
}
#endif


FragmentVertex main_vertex(InputVertex vert)
{
	FragmentVertex result;

	float4 position = float4(vert.position, 1.0);

#if RN_USE_MULTIVIEW
	result.position = mul(viewProjectionMatrix_multiview[vert.viewIndex], mul(vertexInstanceUniforms[vert.instanceID].modelMatrix, position));
#else
	result.position = mul(viewProjectionMatrix, mul(vertexInstanceUniforms[vert.instanceID].modelMatrix, position));
#endif

#if COD_FOG || COD_SHADOWS || COD_ICE || COD_TRIPLANAR
	float4 worldPosition = mul(vertexInstanceUniforms[vert.instanceID].modelMatrix, position);
#endif

#if COD_FOG || COD_SHADOWS || COD_ICE
	result.cameraToVertex.xyz = worldPosition.xyz - cameraPosition;
#endif

#if COD_TRIPLANAR
	result.tiledWorldPositions = worldPosition.xyz * textureTileFactor;
#endif

#if !COD_UNLIT || COD_TRIPLANAR
	float4 normal = float4(vert.normal, 0.0);
	result.worldNormal = mul(vertexInstanceUniforms[vert.instanceID].normalMatrix, normal).xyz;
#endif

#if RN_COLOR
	result.color = vert.color * vertexInstanceUniforms[vert.instanceID].diffuseColor;
#else
	result.color = vertexInstanceUniforms[vert.instanceID].diffuseColor;
#endif

	result.ambientColor = vertexInstanceUniforms[vert.instanceID].ambientColor;

#if COD_STARTFINISH
	result.texCoord0 = vert.position.yy;
#endif

#if COD_UV0 || COD_GRAPPLE_ROPE
	result.texCoord0 = vert.texCoord0;

	#if COD_GRAPPLE_ROPE
	result.texCoord0.y *= textureTileFactor;
	#endif
#endif

#if COD_SHADOWS
	result.shadowPosition[0] = mul(directionalShadowMatrices[0], worldPosition);
	result.shadowPosition[1] = mul(directionalShadowMatrices[1], worldPosition);
	result.shadowPosition[2] = mul(directionalShadowMatrices[2], worldPosition);
	result.shadowPosition[3] = mul(directionalShadowMatrices[3], worldPosition);
#endif

	return result;
}


half4 main_fragment(FragmentVertex vert) : SV_TARGET
{
	half4 color = half4(vert.color);

#if COD_FOG || COD_SHADOWS || COD_ICE
	half3 cameraToVertex = half3(vert.cameraToVertex);
	half distanceToCamera = length(cameraToVertex);
	cameraToVertex = normalize(cameraToVertex);
#endif

#if COD_TRIPLANAR
	// Find our UVs for each axis based on world position of the fragment.
	#if COD_LAVA
		half3 blendNormals = abs(vert.worldNormal);
		float2 finalUV = vert.tiledWorldPositions.xy;
		if(blendNormals.x > blendNormals.y && blendNormals.x > blendNormals.z)
		{
			finalUV = vert.tiledWorldPositions.zy;
			finalUV.x += cos(finalUV.x * 10.0h + time) * 0.02h;
			finalUV.y += sin(finalUV.y * 10.0h + time) * 0.02h + time * 0.02h;
		}
		else if(blendNormals.y > blendNormals.z)
		{
			finalUV = vert.tiledWorldPositions.xz;
			finalUV.x += cos(finalUV.x * 10.0h + time) * 0.02h;
			finalUV.y += sin(finalUV.y * 10.0h + time) * 0.02h - time * 0.02h;
		}
		else
		{
			finalUV.x += cos(finalUV.x * 10.0h + time) * 0.02h;
			finalUV.y += sin(finalUV.y * 10.0h + time) * 0.02h + time * 0.02h;
		}

		color *= texture0.Sample(linearRepeatSampler, finalUV);
	#elif COD_ICE
		half3 blendNormals = abs(vert.worldNormal);
		if(blendNormals.x > blendNormals.y && blendNormals.x > blendNormals.z)
		{
			color.rgb *= texture0.Sample(linearRepeatSampler, vert.tiledWorldPositions.zy).rgb;
		}
		else if(blendNormals.y > blendNormals.z)
		{
			half3 iceColor = texture0.Sample(linearRepeatSampler, vert.tiledWorldPositions.xz).rgb * 0.4h;
			iceColor += texture0.Sample(linearRepeatSampler, vert.tiledWorldPositions.xz + cameraToVertex.xz * 0.025h).rgb * 0.3h;
			iceColor += texture0.Sample(linearRepeatSampler, vert.tiledWorldPositions.xz + cameraToVertex.xz * 0.05h).rgb * 0.3h;
			color.rgb *= iceColor;
		}
		else
		{
			color *= texture0.Sample(linearRepeatSampler, vert.tiledWorldPositions.xy);
		}
	#else
		half3 blendNormals = abs(vert.worldNormal);

		float2 finalUV = lerp(vert.tiledWorldPositions.xy, vert.tiledWorldPositions.xz, (blendNormals.y > blendNormals.z));
		finalUV = lerp(finalUV, vert.tiledWorldPositions.zy, (blendNormals.x > blendNormals.y && blendNormals.x > blendNormals.z));

		color *= texture0.Sample(linearRepeatSampler, finalUV);
	#endif
#elif COD_UV0
	color *= texture0.Sample(linearRepeatSampler, vert.texCoord0);
#elif COD_GRAPPLE_ROPE
	color *= texture0.Sample(linearRepeatSampler, vert.texCoord0);
#endif


	half4 ambientColor = half4(vert.ambientColor);

#if !COD_UNLIT || COD_FOG
	half3 directionalLightDir = half3(directionalLights[0].direction.xyz);
	half4 directionalLightColor = half4(directionalLights[0].color);
#endif

#if COD_STARTFINISH
	half factor = half(1.0 - vert.texCoord0.y);
	factor *= factor * factor;
	factor = saturate(factor);
	color.a = factor;
#elif !COD_UNLIT
	color.rgb *= (ambientColor.rgb + getDirectionalLights(directionalLightDir, directionalLightColor, normalize(half3(vert.worldNormal))
	#if COD_SHADOWS
		, vert.shadowPosition, distanceToCamera
	#endif
	));
#endif

	color.rgb = lerp(half3(1.0h, 1.0h, 1.0h), color.rgb, ambientColor.a);

#if COD_FOG
	half horizonFactor = 1.0h - saturate(abs(cameraToVertex.y) / 0.8h);
	half3 fogColor = lerp(cameraFogColor1.rgb, cameraFogColor0.rgb, horizonFactor * horizonFactor);

	half sunAngle = acos(dot(directionalLightDir, -cameraToVertex));
	half sunSize = 0.05h * directionalLightColor.a;
	half sunGlowSize = directionalLightColor.a;
	half sunFactor = saturate((sunGlowSize - sunAngle) / sunGlowSize);
	sunFactor *= sunFactor;
	fogColor = lerp(fogColor, directionalLightColor.rgb, sunFactor);

	half fogAmount = saturate((1.0h - exp(-distanceToCamera * cameraFogDistance.x))*cameraFogDistance.y);
	color.rgb = lerp(color.rgb, fogColor, fogAmount * fogAmount);
#endif

#if COD_STARTFINISH
	color.rgb *= factor;
#endif

	color.rgb *= half3(cameraAmbientColor.rgb);

	return color;
}
