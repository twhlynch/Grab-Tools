<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
	props: {
		name: String,
		script: String,
	},

	data() {
		return {
			bookmarklet: '(() => {})();',
		};
	},

	async mounted() {
		const path = `/bookmarklets/${this.script}`;

		try {
			const res = await fetch(path);
			const code = await res.text();
			this.bookmarklet = encodeURIComponent(code);
		} catch (_) {
			console.error('Bookmarklet not found:', path);
		}
	},

	methods: {
		click(e: Event) {
			e.preventDefault();
		},
	},
});
</script>

<template>
	<a class="bookmarklet" :href="`javascript:${bookmarklet}`" @click="click">
		<span>{{ name }}</span>
	</a>
</template>
