import { levelNodeWithStatic } from '@/generated/nodes';
import {
	LevelNode,
	LevelNodeMaterial,
	LevelNodeShape,
} from '@/generated/proto';
import { greedy_mesh } from '@/tools/greedy_mesh';
import { describe, expect, it } from 'vitest';

function black(x: number, y: number, z: number) {
	return levelNodeWithStatic({
		material: LevelNodeMaterial.DEFAULT_COLORED,
		shape: LevelNodeShape.CUBE,
		position: { x, y, z },
		color1: { r: 0, g: 0, b: 0, a: 1 },
	});
}

function white(x: number, y: number, z: number) {
	return levelNodeWithStatic({
		material: LevelNodeMaterial.DEFAULT_COLORED,
		shape: LevelNodeShape.CUBE,
		position: { x, y, z },
		color1: { r: 1, g: 1, b: 1, a: 1 },
	});
}

describe('greedy_mesh', () => {
	it('returns empty for empty input', () => {
		expect(greedy_mesh([])).toEqual([]);
	});

	it('leaves a single cube', () => {
		const nodes = [white(0, 0, 0)];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(1);
		expect(result[0]!.levelNodeStatic?.position).toMatchObject({
			x: 0,
			y: 0,
			z: 0,
		});
		expect(result[0]!.levelNodeStatic?.scale).toMatchObject({
			x: 1,
			y: 1,
			z: 1,
		});
	});

	it('merges two cubes along X', () => {
		const nodes = [white(0, 0, 0), white(1, 0, 0)];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(1);
		expect(result[0]!.levelNodeStatic?.position).toMatchObject({
			x: 0.5,
			y: 0,
			z: 0,
		});
		expect(result[0]!.levelNodeStatic?.scale).toMatchObject({
			x: 2,
			y: 1,
			z: 1,
		});
	});

	it('merges two cubes along Y', () => {
		const nodes = [white(0, 0, 0), white(0, 1, 0)];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(1);
		expect(result[0]!.levelNodeStatic?.position).toMatchObject({
			x: 0,
			y: 0.5,
			z: 0,
		});
		expect(result[0]!.levelNodeStatic?.scale).toMatchObject({
			x: 1,
			y: 2,
			z: 1,
		});
	});

	it('merges two cubes along Z', () => {
		const nodes = [white(0, 0, 0), white(0, 0, 1)];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(1);
		expect(result[0]!.levelNodeStatic?.position).toMatchObject({
			x: 0,
			y: 0,
			z: 0.5,
		});
		expect(result[0]!.levelNodeStatic?.scale).toMatchObject({
			x: 1,
			y: 1,
			z: 2,
		});
	});

	it('merges a 2x2x2 block', () => {
		const nodes: LevelNode[] = [];
		for (let x = 0; x < 2; x++) {
			for (let y = 0; y < 2; y++) {
				for (let z = 0; z < 2; z++) {
					nodes.push(white(x, y, z));
				}
			}
		}
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(1);
		expect(result[0]!.levelNodeStatic?.position).toMatchObject({
			x: 0.5,
			y: 0.5,
			z: 0.5,
		});
		expect(result[0]!.levelNodeStatic?.scale).toMatchObject({
			x: 2,
			y: 2,
			z: 2,
		});
	});

	it('does not merge non adjacent cubes', () => {
		const nodes = [white(0, 0, 0), white(2, 0, 0)];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(2);
	});

	it('does not merge different colors', () => {
		const nodes = [white(0, 0, 0), black(1, 0, 0)];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(2);
	});

	it('merges different colors separately', () => {
		const nodes = [
			white(0, 0, 0),
			white(1, 0, 0),
			black(0, 1, 0),
			black(1, 1, 0),
		];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(2);
	});

	it('handles an L shape', () => {
		const nodes = [
			white(0, 0, 0),
			white(1, 0, 0),
			white(2, 0, 0),
			white(0, 1, 0),
		];
		const result = greedy_mesh(nodes);
		expect(result).toHaveLength(2);
	});
});
