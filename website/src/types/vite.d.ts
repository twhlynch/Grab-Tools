declare module '*?raw' {
	const value: string;
	export default value;
}

declare module '*.css' {}

declare module '*.gltf' {
	const src: string;
	export default src;
}

declare module '*.glb' {
	const src: string;
	export default src;
}

declare module '*.png' {
	const src: string;
	export default src;
}

declare module '*.vue' {
	import type { DefineComponent } from 'vue';
	const component: DefineComponent<object, object, unknown>;
	export default component;
}
