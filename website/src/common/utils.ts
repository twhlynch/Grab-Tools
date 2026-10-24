import { unmodded_root } from '@/common/root';
import {
	Level,
	LevelNode,
	LevelNodeMaterial,
	LevelNodeShape,
} from '@grab-tools/lib/generated/proto';
import { Object3D } from 'three';

export function isObject3D(object: unknown): object is Object3D {
	return object instanceof Object3D;
}

export function materials() {
	return unmodded_root().COD.Level.LevelNodeMaterial;
}

export function shapes() {
	return unmodded_root().COD.Level.LevelNodeShape;
}

export function deepClone<T>(node: T): T {
	return JSON.parse(JSON.stringify(node)) as T;
}

export function traverse_node(node: LevelNode, func: (n: LevelNode) => void) {
	if (node.levelNodeGroup?.childNodes?.length) {
		node.levelNodeGroup.childNodes.forEach((child) =>
			traverse_node(child, func),
		);
	}
	func(node);
}

export function random_material(): LevelNodeMaterial {
	const options = Object.values(materials());
	options.filter((option) => option !== materials().TRIGGER);
	const length = options.length;
	return options[Math.floor(Math.random() * length)] as LevelNodeMaterial;
}
export function random_shape(): LevelNodeShape {
	const length =
		Object.entries(shapes()).length - shapes().__END_OF_SPECIAL_PARTS__ - 1;
	return 1000 + Math.floor(Math.random() * length);
}

export function add_nodes(level: Level, nodes: LevelNode[] | undefined) {
	(level.levelNodes ??= []).push(...(nodes ?? []));
}

export function json_parse<T>(text: string): T | null {
	try {
		return JSON.parse(text) as T;
	} catch (e) {
		if (e instanceof Error) {
			e.message = 'Invalid JSON: ' + e.message;
			window.toast(e, 'error');
		}
		return null;
	}
}
