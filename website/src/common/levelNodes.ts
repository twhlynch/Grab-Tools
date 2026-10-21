import {
	LevelNodeKey,
	LevelNodeTypes,
	LevelNodeWith,
} from '@grab-tools/lib/common/levelNodes';
import {
	Animation,
	InstructionDataType,
	LevelNode,
	LevelNodeMaterial,
	LevelNodeShape,
	OperandDataType,
} from '@grab-tools/lib/generated/proto';
import { Root as PBRoot, Type } from 'protobufjs';
import {
	IUniform,
	Mesh,
	Object3D,
	Quaternion,
	ShaderMaterial,
	Vector3,
} from 'three';
import { isObject3D } from './utils';

// bidirectional map from enum
type EnumMap<E> = {
	[K in keyof E as K extends string ? K : never]: E[K];
} & Record<E[keyof E] & number, keyof E> &
	Record<string, number | keyof E>;

// protobuf.Root with assumed
export type Root = PBRoot & {
	COD: {
		Level: {
			LevelNode: Type & {
				oneofs: { content: { fieldsArray: { name: LevelNodeKey }[] } };
			};
			LevelNodeMaterial: Record<string, LevelNodeMaterial>;
			LevelNodeShape: Record<string, LevelNodeShape>;
			InstructionData: {
				Type: EnumMap<typeof InstructionDataType>;
			};
			OperandData: {
				Type: EnumMap<typeof OperandDataType>;
			};
		};
	};
};

// object type
// - all of Object3D
// - optionally Mesh exclusing material
// - shader material
// - other custom properties
// - is<Node>
export type LevelNodeObject<T extends LevelNodeTypes = never> = Partial<
	Omit<Mesh, 'material' | keyof Object3D>
> &
	Object3D & {
		material?: ShaderMaterial & {
			uniforms: {
				fogEnabled: IUniform<number>;
				isSelected: IUniform<boolean>;
			};
		};
		initialPosition: Vector3;
		initialRotation: Quaternion;
		userData: {
			id: number;
			node: [T] extends [never] ? LevelNode : LevelNodeWith<T>;
			animation?: Animation;
			currentFrameIndex?: number;
			update?: (delta: number) => void;
		} & {
			[
				K in LevelNodeKey as K extends `levelNode${infer S}`
					? `is${S}`
					: K
			]?: boolean;
		};
	};

// type guards for LevelNodeObjects
export function isLevelNodeObject(object: unknown): object is LevelNodeObject {
	return isObject3D(object) && 'node' in object.userData;
}
