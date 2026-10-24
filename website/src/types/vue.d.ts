import 'vue';

declare module 'vue' {
	interface ComponentCustomProperties {
		$config: typeof import('@/config');
	}
}
