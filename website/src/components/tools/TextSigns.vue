<script lang="ts">
import { createLevel, downloadLevel, encodeLevel } from '@/common/levels';
import signs from '@/tools/signs';
import { defineComponent } from 'vue';
import ToolTemplate from './ToolTemplate.vue';

export default defineComponent({
	components: {
		ToolTemplate,
	},
	methods: {
		run() {
			const textInput = this.$refs.text as HTMLInputElement;
			const modeInput = this.$refs.mode as HTMLInputElement;

			const text = textInput.value;
			const mode = modeInput.value;

			const nodes = signs.signs(text, mode === 'animated');

			const level = createLevel(nodes, 'Signs', 'Generated with GRAB Tools', [
				'.index',
				'GRAB Tools',
			]);

			const encoded = encodeLevel(level);
			if (!encoded) return;

			downloadLevel(encoded);
		},
	},
});
</script>

<template>
	<ToolTemplate
		:name="'Text to Signs'"
		:details="'Generate a list of signs or an animated playback of text.'"
	>
		<textarea ref="text" cols="30" rows="5" placeholder="text"></textarea>
		<select ref="mode">
			<option value="simple" selected>simple</option>
			<option value="animated">animated</option>
		</select>
		<button class="button" @click="run">Generate</button>
	</ToolTemplate>
</template>
