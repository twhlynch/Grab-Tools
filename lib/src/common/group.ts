import { levelNodeData, levelNodeWithGroup } from '../generated/nodes';
import { LevelNode, LevelNodeGroup, Vector } from '../generated/proto';

export function levelNodeGroupFrom(
	overrides: Partial<LevelNodeGroup> &
		Required<Pick<LevelNodeGroup, 'childNodes'>>,
) {
	const center = get_nodes_center(overrides.childNodes);
	place_nodes_around(overrides.childNodes, center);

	return levelNodeWithGroup({
		position: center,
		...overrides,
	});
}

export function place_nodes_around(nodes: LevelNode[], center: Vector) {
	nodes.forEach((node) => {
		const data = levelNodeData(node);

		data.position ??= {};
		data.position.x = (data.position.x ?? 0) - (center.x ?? 0);
		data.position.y = (data.position.y ?? 0) - (center.y ?? 0);
		data.position.z = (data.position.z ?? 0) - (center.z ?? 0);
	});
}

export function get_nodes_center(nodes: LevelNode[]): Vector {
	const positions = nodes.map((node) => {
		const data = levelNodeData(node);

		return {
			x: data.position?.x ?? 0,
			y: data.position?.y ?? 0,
			z: data.position?.z ?? 0,
		};
	});

	const min = { x: Infinity, y: Infinity, z: Infinity };
	const max = { x: -Infinity, y: -Infinity, z: -Infinity };

	for (const position of positions) {
		min.x = Math.min(min.x, position.x);
		min.y = Math.min(min.y, position.y);
		min.z = Math.min(min.z, position.z);

		max.x = Math.max(max.x, position.x);
		max.y = Math.max(max.y, position.y);
		max.z = Math.max(max.z, position.z);
	}

	const center = {
		x: (min.x + max.x) / 2,
		y: (min.y + max.y) / 2,
		z: (min.z + max.z) / 2,
	};

	return { x: center.x, y: center.y, z: center.z };
}
