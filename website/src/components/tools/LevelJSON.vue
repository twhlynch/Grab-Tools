<script lang="ts">
import { decodeLevel, downloadJSON, downloadLevel, encodeLevel } from '@/common/levels';
import { defineComponent } from 'vue';
import ToolTemplate from './ToolTemplate.vue';

export default defineComponent({
	components: {
		ToolTemplate,
	},
	methods: {
		async run() {
			const fileInput = this.$refs.file as HTMLInputElement;

			const files = Array.from(fileInput.files ?? []);
			const file = files[0];
			if (!file) {
				window.toast('No file chosen', 'error');
				return;
			}

			files
				.filter((f) => f.name.endsWith('.json'))
				.forEach(async (f) => {
					const json = JSON.parse(await f.text());
					const level = encodeLevel(json);
					if (level) downloadLevel(level, f.name.replace(/\.(json|level)/, ''));
				});
			files
				.filter((f) => f.name.endsWith('.level'))
				.forEach(async (f) => {
					const json = await decodeLevel(f);
					if (!json) return;
					downloadJSON(json, f.name.replace(/\.(json|level)/, ''));
				});
		},
	},
});
</script>

<template>
	<ToolTemplate
		:name="'Level to JSON'"
		:details="'Convert a levels to readable JSON data and back.'"
	>
		<input ref="file" type="file" accept=".level,.json" multiple />
		<button class="button" @click="run">Convert</button>
	</ToolTemplate>
</template>
