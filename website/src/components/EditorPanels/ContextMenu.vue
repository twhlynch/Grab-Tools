<script lang="ts">
import { defineComponent, PropType } from 'vue';
import DropDown from './DropDown.vue';
import { Menu } from './menu';

export default defineComponent({
	components: {
		DropDown,
	},
	props: {
		menu: {
			type: Object as PropType<Menu>,
			required: true,
		},
	},
	emits: ['close'],
	methods: {
		close() {
			this.$emit('close');
		},
	},
});
</script>

<template>
	<section>
		<DropDown :menu="menu" :callback="close" class="menu" />
	</section>
</template>

<style scoped>
section {
	position: fixed;
	width: fit-content;
	height: fit-content;
	z-index: 2000;
	-webkit-user-select: none;
	user-select: none;
}
.menu {
	display: block;
}
</style>
