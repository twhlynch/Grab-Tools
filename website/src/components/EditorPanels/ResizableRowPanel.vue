<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
	emits: ['resize'],
	data() {
		return {
			down: false,
		};
	},
	mounted() {
		document.addEventListener('mouseup', this.mouseup.bind(this));
		document.addEventListener('mousemove', this.mousemove.bind(this));
		window.addEventListener('resize', this.resize.bind(this));
	},
	unmounted() {
		document.removeEventListener('mouseup', this.mouseup.bind(this));
		document.removeEventListener('mousemove', this.mousemove.bind(this));
		window.removeEventListener('resize', this.resize.bind(this));
	},
	methods: {
		mousedown(_: MouseEvent) {
			this.down = true;
			document.addEventListener('selectstart', this.prevent.bind(this));
		},
		mouseup(_: MouseEvent) {
			this.down = false;
			document.removeEventListener('selectstart', this.prevent.bind(this));
		},
		mousemove(e: MouseEvent) {
			if (this.down) {
				this.size(e.clientX);
			}
		},
		size(position?: number) {
			const { container, first, second, thumb } = this.$refs as Record<string, HTMLElement>;
			position ??= thumb!.getBoundingClientRect().left;
			const bounds = container!.getBoundingClientRect();
			first!.style.width = position - bounds.left + 'px';
			second!.style.width = bounds.width - (position - bounds.left) - 5 + 'px';
			this.$emit('resize');
		},
		prevent(e: Event) {
			e.preventDefault();
		},
		resize() {
			const thumb = this.$refs.thumb as HTMLElement;
			const position = thumb.getBoundingClientRect().left;
			this.size(position);
		},
	},
});
</script>

<template>
	<section :ref="'container'" class="container">
		<div :ref="'first'" class="first">
			<slot name="first" />
		</div>
		<div :ref="'thumb'" class="thumb" @mousedown="mousedown"></div>
		<div :ref="'second'" class="second">
			<slot name="second" />
		</div>
	</section>
</template>

<style scoped>
.container {
	display: flex;
	flex-direction: row;
}
.first,
.second {
	height: 100%;
	width: 50%;
}
.second {
	width: calc(50% - 5px);
}
.thumb {
	height: 100%;
	background: #424243;
	width: 5px;
	cursor: col-resize;
}
</style>
