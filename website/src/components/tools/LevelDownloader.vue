<script lang="ts">
import { defineComponent } from 'vue';
import ToolTemplate from './ToolTemplate.vue';

export default defineComponent({
	components: {
		ToolTemplate,
	},
	data() {
		return {
			download_link: '/download',
		};
	},
	methods: {
		change() {
			const urlsInput = this.$refs.urls as HTMLInputElement;

			const links = urlsInput.value
				.split(',')
				.map((link) => link.trim().split('=')[1])
				.join('+');

			this.download_link = `/download?level=${links}`;
		},
	},
});
</script>

<template>
	<ToolTemplate
		:name="'Level Downloader'"
		:details="'Paste a list of level browser links to your levels to download them.'"
	>
		<textarea
			id="urls"
			cols="30"
			rows="5"
			placeholder="link, link, link, link"
			@change="change"
		></textarea>
		<a class="button" :href="download_link">Download</a>
	</ToolTemplate>
</template>
