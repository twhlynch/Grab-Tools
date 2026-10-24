<script lang="ts">
import { downloadLevel } from '@/common/levels';
import { useUserStore } from '@/stores/user';
import downloads from '@/tools/downloads';
import { mapState } from 'pinia';
import { defineComponent } from 'vue';

export default defineComponent({
	computed: {
		...mapState(useUserStore, ['is_logged_in', 'user_name']),
	},
	mounted() {
		const url_params = new URLSearchParams(window.location.search);
		const level_ids = url_params.get('level');
		if (!level_ids) return;

		async function download_level(level_id: string): Promise<void> {
			const level = await downloads.try_download_level(level_id);
			if (level === null) return;
			downloadLevel(level, level_id);
		}

		level_ids.split(' ').forEach((level_id) => {
			void download_level(level_id);
		});
	},
	created() {
		document.title = 'Download | GRAB Tools';
	},
});
</script>

<template>
	<main>
		<section>
			<h2>Downloading</h2>
			<p>Downloading the level...</p>
		</section>
	</main>
</template>

<style scoped>
main {
	justify-items: center;
}
section {
	max-width: fit-content;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}
</style>
