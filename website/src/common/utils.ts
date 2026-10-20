import {
	isLevelNodeObject,
	LevelNodeObject,
	LevelNodeTypes,
} from '@/common/levelNodes';
import { unmodded_root } from '@/common/root';
import {
	Level,
	LevelNode,
	LevelNodeMaterial,
	LevelNodeShape,
} from '@/generated/proto';
import { Object3D } from 'three';

export function isObject3D(object: unknown): object is Object3D {
	return object instanceof Object3D;
}

export function materials(): Record<string, LevelNodeMaterial> {
	return unmodded_root().COD.Level.LevelNodeMaterial;
}

export function shapes(): Record<string, LevelNodeShape> {
	return unmodded_root().COD.Level.LevelNodeShape;
}

export function node_data(object: LevelNode | LevelNodeObject): LevelNodeTypes {
	const node: LevelNode = isLevelNodeObject(object)
		? object.userData.node
		: object;
	const entries = Object.entries(node);

	const data = entries.find((e) =>
		e[0].includes('levelNode'),
	)?.[1] as LevelNodeTypes;

	return data;
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

export function random_material() {
	const options = Object.values(materials());
	options.filter((option) => option !== materials().TRIGGER);
	const length = options.length;
	return options[Math.floor(Math.random() * length)];
}
export function random_shape() {
	const length =
		Object.entries(shapes()).length -
		(shapes().__END_OF_SPECIAL_PARTS__ ?? 0) -
		1;
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
