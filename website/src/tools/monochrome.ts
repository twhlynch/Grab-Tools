import { traverse_node } from '@/common/utils';
import {
	Color,
	LevelNode,
	LevelNodeMaterial,
} from '@grab-tools/lib/generated/proto';

export function monochrome(nodes: LevelNode[]) {
	nodes.forEach((n) => {
		traverse_node(n, (node) => {
			const static_node = node.levelNodeStatic;
			if (static_node?.material !== LevelNodeMaterial.DEFAULT_COLORED)
				return;
			if (static_node.color1) {
				monochrom_color(static_node.color1);
			}
			if (static_node.color2) {
				monochrom_color(static_node.color2);
			}
		});
	});

	return nodes;
}

function monochrom_color(color: Color) {
	const r = color.r ?? 0;
	const g = color.g ?? 0;
	const b = color.b ?? 0;

	const brightness = Math.sqrt(
		0.299 * Math.pow(r, 2) +
			0.587 * Math.pow(g, 2) +
			0.114 * Math.pow(b, 2),
	);

	color.r = brightness;
	color.g = brightness;
	color.b = brightness;
}
