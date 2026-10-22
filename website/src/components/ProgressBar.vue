<script>
export default {
	props: {
		progress: Number,
	},
};
</script>

<template>
	<div v-show="progress !== 0" class="progress-bar">
		<div class="progress" :style="`width: ${progress}%;`"></div>
	</div>
</template>

<style scoped>
.progress-bar {
	height: 5px;
	width: 100%;
	background-color: var(--border-color);
	border-radius: 5px;
	display: flex;
}
.progress {
	background-color: var(--text-color-accent);
	height: 100%;
	width: 0;
	border-radius: 5px;
	margin-right: auto;
}
</style>
