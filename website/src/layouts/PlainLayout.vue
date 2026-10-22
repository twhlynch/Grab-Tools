<script>
export default {};
</script>

<template>
	<div class="plain-layout">
		<router-view />
	</div>
</template>

<style>
body:has(.plain-layout) {
	width: 100vw;
	height: 100vh;
	font-size: var(--font-size-default);
	font-family: var(--font-family-default);
	color: var(--text-color-default);
}
.plain-layout {
	width: 100vw;
	height: 100vh;

	svg {
		height: 24px;
		width: 24px;
		color: var(--text-color-default);
	}
}
</style>
