import ViewportPanel from '@/components/EditorPanels/ViewportPanel.vue';
import * as THREE from 'three';

// TODO: correctly use raw properties to get inference
// for now just update this as needed
export type Viewport = InstanceType<typeof ViewportPanel> & {
	gizmo: {
		empty(): boolean;
		clear(): void;
		selection: THREE.Object3D[];
	};
	renderer: { domElement: HTMLElement };
	camera: THREE.Camera;
	level: {
		nodes: { all: THREE.Object3D[] };
		scene: THREE.Scene;
	};
	editing_parent: THREE.Object3D | null;
	modifier(fn: (json: unknown) => unknown): void;
};

export interface Tool {
	readonly name: string;

	// return 'success'
	activate(viewport: Viewport): boolean;
	deactivate?(): void;

	// return 'handled' to prevent default handling
	on_click?(e: MouseEvent): boolean;
	on_mouse_down?(e: MouseEvent): boolean;
	on_mouse_up?(e: MouseEvent): boolean;
	on_mouse_move?(e: MouseEvent): boolean;
	on_contextmenu?(e: MouseEvent): boolean;
	on_key_down?(e: KeyboardEvent): boolean;
	on_key_up?(e: KeyboardEvent): boolean;
}
