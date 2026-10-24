<script lang="ts">
import { LevelNodeObject } from '@/common/levelNodes';
import { materials, shapes } from '@/common/utils';
import { LevelData } from '@/editor/LevelLoader';
import StatsIcon from '@/icons/StatsIcon.vue';
import { LevelNodeKey } from '@grab-tools/lib/generated/nodes';
import { LevelNodeMaterial, LevelNodeShape } from '@grab-tools/lib/generated/proto';
import { defineComponent } from 'vue';

type LevelNodeSuffix = LevelNodeKey extends `levelNode${infer S}` ? S : never;

type TitleCase<S extends string> = S extends `${infer First}${infer Rest}`
	? `${First}${Lowercase<Rest>}`
	: S;

type EnumLabel<T extends Record<string, string | number>> = {
	[K in keyof T]: `${TitleCase<K & string>} (${T[K]})`;
}[keyof T];

type LevelNodeShapeLabel = EnumLabel<typeof LevelNodeShape>;
type LevelNodeMaterialLabel = EnumLabel<typeof LevelNodeMaterial>;

export default defineComponent({
	components: {
		StatsIcon,
	},
	data() {
		return {
			statistics: {
				Objects: 0,
				Complexity: 0,
				'JSON Lines': 0,
				Animations: 0,
				Connections: 0,
				Frames: 0,
			},
			extra_statistics: {} as Record<
				LevelNodeSuffix | LevelNodeShapeLabel | LevelNodeMaterialLabel,
				number
			>,
			show_extra: false,
		};
	},
	methods: {
		set_level(level: LevelData) {
			this.statistics.Complexity = level.complexity;
			this.statistics.Animations = level.nodes.animated.flatMap(
				(object) => object.userData.node.animations,
			).length;
			this.statistics.Connections = level.nodes.levelNodeTrigger.flatMap(
				(object) => object.userData.node.levelNodeTrigger.triggerTargets,
			).length;
			this.statistics.Frames = level.nodes.animated.flatMap((object) =>
				(object.userData.node.animations ?? []).flatMap((animation) => animation.frames),
			).length;
			this.statistics['JSON Lines'] = JSON.stringify(level.level, null, 1).split('\n').length;
			this.statistics.Objects = level.nodes.all.length;

			for (const key in level.nodes) {
				if (key.includes('levelNode')) {
					this.extra_statistics[`${key.replace('levelNode', '')}` as LevelNodeSuffix] =
						level.nodes[key as LevelNodeKey].length;
				}
			}

			for (const [shape, objects] of Object.entries(level.nodes.shape) as [
				`${LevelNodeShape}`,
				LevelNodeObject[],
			][]) {
				const name = Object.keys(shapes()).find(
					(k) => shapes()[k as keyof typeof LevelNodeShape] === Number(shape),
				) as keyof typeof LevelNodeShape | undefined;

				if (!name || Number(shape) < LevelNodeShape.CUBE) continue;

				const enumValue = LevelNodeShape[name];
				const nameFmt = (name.charAt(0) + name.toLowerCase().slice(1)) as TitleCase<
					typeof name
				>;
				const label = `${nameFmt} (${enumValue})` as LevelNodeShapeLabel;

				this.extra_statistics[label] = objects.length;
			}

			for (const [material, objects] of Object.entries(level.nodes.material) as [
				`${LevelNodeMaterial}`,
				LevelNodeObject[],
			][]) {
				const name = Object.keys(materials()).find(
					(k) => materials()[k as keyof typeof LevelNodeMaterial] === Number(material),
				) as keyof typeof LevelNodeMaterial | undefined;

				if (!name || Number(material) === LevelNodeMaterial.TRIGGER) continue;

				const enumValue = LevelNodeMaterial[name];
				const nameFmt = (name.charAt(0) + name.toLowerCase().slice(1)) as TitleCase<
					typeof name
				>;
				const label = `${nameFmt} (${enumValue})` as LevelNodeMaterialLabel;

				this.extra_statistics[label] = objects.length;
			}
		},
		click() {
			this.show_extra = !this.show_extra;
		},
	},
});
</script>

<template>
	<section id="statistics-panel">
		<button @click="click">
			<StatsIcon class="stats-icon" />
		</button>
		<div v-for="[key, value] of Object.entries(statistics)" :key="key" class="statistic">
			<span>{{ key }}</span>
			:
			<span>{{ value }}</span>
		</div>
		<div v-show="show_extra" class="extra">
			<div v-for="[key, value] of Object.entries(extra_statistics)" :key="key">
				<span>{{ key }}</span>
				:
				<span>{{ value }}</span>
			</div>
		</div>
	</section>
</template>

<style scoped>
.stats-icon {
	width: 80%;
	height: 80%;
}
#statistics-panel > button {
	cursor: pointer;
	color: var(--text-color-default);
}
section {
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: row;
	gap: 0.1rem;
}
.extra {
	display: flex;
	flex-direction: column;
	position: absolute;
	left: 0.2rem;
	bottom: 1.2rem;
	color: white;
}
button {
	height: 100%;
	aspect-ratio: 1 / 1;
	background-color: var(--bg);
}
.statistic {
	height: 100%;
	border-right: 1px solid #fff3;
	padding-inline: 0.5rem;
}
</style>
