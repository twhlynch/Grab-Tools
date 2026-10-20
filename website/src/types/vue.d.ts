import 'vue';

declare module 'vue' {
	interface ComponentCustomProperties {
		$config: typeof import('@/config');
	}
}

declare module '*.vue' {
	import type { DefineComponent } from 'vue';
	const component: DefineComponent<object, object, unknown>;
	export default component;
}
