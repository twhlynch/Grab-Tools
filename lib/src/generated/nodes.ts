import {
	levelNode,
	levelNodeCrumbling,
	levelNodeFinish,
	levelNodeGASM,
	levelNodeGravity,
	levelNodeGroup,
	levelNodeLight,
	levelNodeLobbyTerminal,
	levelNodeParticleEmitter,
	levelNodeSign,
	levelNodeSound,
	levelNodeStart,
	levelNodeStatic,
	levelNodeTrigger,
	triggerSource,
	triggerSourceBasic,
	triggerSourceBlockNames,
	triggerTarget,
	triggerTargetAmbience,
	triggerTargetAnimation,
	triggerTargetGASM,
	triggerTargetLight,
	triggerTargetSound,
	triggerTargetSubLevel,
} from './helpers';
import {
	LevelNode,
	LevelNodeCrumbling,
	LevelNodeFinish,
	LevelNodeGASM,
	LevelNodeGravity,
	LevelNodeGroup,
	LevelNodeLight,
	LevelNodeLobbyTerminal,
	LevelNodeParticleEmitter,
	LevelNodeSign,
	LevelNodeSound,
	LevelNodeStart,
	LevelNodeStatic,
	LevelNodeTrigger,
	TriggerSource,
	TriggerSourceBasic,
	TriggerSourceBlockNames,
	TriggerTarget,
	TriggerTargetAmbience,
	TriggerTargetAnimation,
	TriggerTargetGASM,
	TriggerTargetLight,
	TriggerTargetSound,
	TriggerTargetSubLevel,
} from './proto';

import { KeyMapping, KeysOfType, PropsStartingWith, TypesExcept } from './util';

export type LevelNodeWith<T> = LevelNode &
	Record<KeysOfType<LevelNode, T, 'levelNode'>, T>;
export type LevelNodeTypes = NonNullable<
	PropsStartingWith<LevelNode, 'levelNode'>
>;

export type LevelNodeKey = keyof KeyMapping<LevelNode, 'levelNode'>;
export type LevelNodeTypeFor<K extends LevelNodeKey> = KeyMapping<
	LevelNode,
	'levelNode'
>[K];

export type LevelNodeTypesExcept<T extends LevelNodeTypes[]> = TypesExcept<
	LevelNode,
	'levelNode',
	LevelNodeTypes,
	T
>;

export function levelNodeWith<T extends LevelNodeTypes>(
	nodeData: Partial<LevelNodeWith<T>>,
): LevelNodeWith<T> {
	return levelNode(nodeData) as LevelNodeWith<T>;
}
export type LevelNodeWithAny = {
	[K in LevelNodeKey]: LevelNodeWith<LevelNodeTypeFor<K>>;
}[LevelNodeKey];

export function levelNodeData<T extends LevelNodeTypes>(
	node: LevelNodeWith<T>,
): T;
export function levelNodeData(node: LevelNodeWithAny): LevelNodeTypes;
export function levelNodeData(node: LevelNode): LevelNodeTypes | undefined;
export function levelNodeData(node: LevelNode): LevelNodeTypes | undefined {
	return Object.entries(node).find(
		([key, val]) => key.startsWith('levelNode') && !!val,
	)?.[1] as LevelNodeTypes | undefined;
}

export function isLevelNode<K extends LevelNodeKey>(
	node: LevelNode,
	key: K,
): node is LevelNodeWith<LevelNodeTypeFor<K>>;
export function isLevelNode(node: LevelNode): node is LevelNodeWithAny;
export function isLevelNode(node: LevelNode, key?: LevelNodeKey): boolean {
	if (key !== undefined) {
		return !!node[key];
	}
	return Object.entries(node).some(
		([k, v]) => k.startsWith('levelNode') && !!v,
	);
}

export type TriggerSourceWith<T> = TriggerSource &
	Record<KeysOfType<TriggerSource, T, 'triggerSource'>, T>;
export type TriggerSourceTypes = NonNullable<
	PropsStartingWith<TriggerSource, 'triggerSource'>
>;

export type TriggerSourceKey = keyof KeyMapping<TriggerSource, 'triggerSource'>;
export type TriggerSourceTypeFor<K extends TriggerSourceKey> = KeyMapping<
	TriggerSource,
	'triggerSource'
>[K];

export type TriggerSourceTypesExcept<T extends TriggerSourceTypes[]> =
	TypesExcept<TriggerSource, 'triggerSource', TriggerSourceTypes, T>;

export function triggerSourceWith<T extends TriggerSourceTypes>(
	nodeData: Partial<TriggerSourceWith<T>>,
): TriggerSourceWith<T> {
	return triggerSource(nodeData) as TriggerSourceWith<T>;
}
export type TriggerSourceWithAny = {
	[K in TriggerSourceKey]: TriggerSourceWith<TriggerSourceTypeFor<K>>;
}[TriggerSourceKey];

export function triggerSourceData<T extends TriggerSourceTypes>(
	node: TriggerSourceWith<T>,
): T;
export function triggerSourceData(
	node: TriggerSourceWithAny,
): TriggerSourceTypes;
export function triggerSourceData(
	node: TriggerSource,
): TriggerSourceTypes | undefined;
export function triggerSourceData(
	node: TriggerSource,
): TriggerSourceTypes | undefined {
	return Object.entries(node).find(
		([key, val]) => key.startsWith('triggerSource') && !!val,
	)?.[1] as TriggerSourceTypes | undefined;
}

export function isTriggerSource<K extends TriggerSourceKey>(
	node: TriggerSource,
	key: K,
): node is TriggerSourceWith<TriggerSourceTypeFor<K>>;
export function isTriggerSource(
	node: TriggerSource,
): node is TriggerSourceWithAny;
export function isTriggerSource(
	node: TriggerSource,
	key?: TriggerSourceKey,
): boolean {
	if (key !== undefined) {
		return !!node[key];
	}
	return Object.entries(node).some(
		([k, v]) => k.startsWith('triggerSource') && !!v,
	);
}

export type TriggerTargetWith<T> = TriggerTarget &
	Record<KeysOfType<TriggerTarget, T, 'triggerTarget'>, T>;
export type TriggerTargetTypes = NonNullable<
	PropsStartingWith<TriggerTarget, 'triggerTarget'>
>;

export type TriggerTargetKey = keyof KeyMapping<TriggerTarget, 'triggerTarget'>;
export type TriggerTargetTypeFor<K extends TriggerTargetKey> = KeyMapping<
	TriggerTarget,
	'triggerTarget'
>[K];

export type TriggerTargetTypesExcept<T extends TriggerTargetTypes[]> =
	TypesExcept<TriggerTarget, 'triggerTarget', TriggerTargetTypes, T>;

export function triggerTargetWith<T extends TriggerTargetTypes>(
	nodeData: Partial<TriggerTargetWith<T>>,
): TriggerTargetWith<T> {
	return triggerTarget(nodeData) as TriggerTargetWith<T>;
}
export type TriggerTargetWithAny = {
	[K in TriggerTargetKey]: TriggerTargetWith<TriggerTargetTypeFor<K>>;
}[TriggerTargetKey];

export function triggerTargetData<T extends TriggerTargetTypes>(
	node: TriggerTargetWith<T>,
): T;
export function triggerTargetData(
	node: TriggerTargetWithAny,
): TriggerTargetTypes;
export function triggerTargetData(
	node: TriggerTarget,
): TriggerTargetTypes | undefined;
export function triggerTargetData(
	node: TriggerTarget,
): TriggerTargetTypes | undefined {
	return Object.entries(node).find(
		([key, val]) => key.startsWith('triggerTarget') && !!val,
	)?.[1] as TriggerTargetTypes | undefined;
}

export function isTriggerTarget<K extends TriggerTargetKey>(
	node: TriggerTarget,
	key: K,
): node is TriggerTargetWith<TriggerTargetTypeFor<K>>;
export function isTriggerTarget(
	node: TriggerTarget,
): node is TriggerTargetWithAny;
export function isTriggerTarget(
	node: TriggerTarget,
	key?: TriggerTargetKey,
): boolean {
	if (key !== undefined) {
		return !!node[key];
	}
	return Object.entries(node).some(
		([k, v]) => k.startsWith('triggerTarget') && !!v,
	);
}

export function levelNodeWithGroup(overrides?: Partial<LevelNodeGroup>) {
	return levelNodeWith({
		levelNodeGroup: levelNodeGroup(overrides),
	});
}
export function isLevelNodeGroup(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeGroup> {
	return 'levelNodeGroup' in node;
}

export function levelNodeWithStart(overrides?: Partial<LevelNodeStart>) {
	return levelNodeWith({
		levelNodeStart: levelNodeStart(overrides),
	});
}
export function isLevelNodeStart(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeStart> {
	return 'levelNodeStart' in node;
}

export function levelNodeWithFinish(overrides?: Partial<LevelNodeFinish>) {
	return levelNodeWith({
		levelNodeFinish: levelNodeFinish(overrides),
	});
}
export function isLevelNodeFinish(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeFinish> {
	return 'levelNodeFinish' in node;
}

export function levelNodeWithStatic(overrides?: Partial<LevelNodeStatic>) {
	return levelNodeWith({
		levelNodeStatic: levelNodeStatic(overrides),
	});
}
export function isLevelNodeStatic(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeStatic> {
	return 'levelNodeStatic' in node;
}

export function levelNodeWithCrumbling(
	overrides?: Partial<LevelNodeCrumbling>,
) {
	return levelNodeWith({
		levelNodeCrumbling: levelNodeCrumbling(overrides),
	});
}
export function isLevelNodeCrumbling(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeCrumbling> {
	return 'levelNodeCrumbling' in node;
}

export function levelNodeWithSign(overrides?: Partial<LevelNodeSign>) {
	return levelNodeWith({
		levelNodeSign: levelNodeSign(overrides),
	});
}
export function isLevelNodeSign(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeSign> {
	return 'levelNodeSign' in node;
}

export function levelNodeWithGravity(overrides?: Partial<LevelNodeGravity>) {
	return levelNodeWith({
		levelNodeGravity: levelNodeGravity(overrides),
	});
}
export function isLevelNodeGravity(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeGravity> {
	return 'levelNodeGravity' in node;
}

export function levelNodeWithLobbyTerminal(
	overrides?: Partial<LevelNodeLobbyTerminal>,
) {
	return levelNodeWith({
		levelNodeLobbyTerminal: levelNodeLobbyTerminal(overrides),
	});
}
export function isLevelNodeLobbyTerminal(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeLobbyTerminal> {
	return 'levelNodeLobbyTerminal' in node;
}

export function levelNodeWithParticleEmitter(
	overrides?: Partial<LevelNodeParticleEmitter>,
) {
	return levelNodeWith({
		levelNodeParticleEmitter: levelNodeParticleEmitter(overrides),
	});
}
export function isLevelNodeParticleEmitter(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeParticleEmitter> {
	return 'levelNodeParticleEmitter' in node;
}

export function triggerSourceWithBasic(
	overrides?: Partial<TriggerSourceBasic>,
) {
	return triggerSourceWith({
		triggerSourceBasic: triggerSourceBasic(overrides),
	});
}
export function isTriggerSourceBasic(
	node: TriggerSource,
): node is TriggerSourceWith<TriggerSourceBasic> {
	return 'triggerSourceBasic' in node;
}

export function triggerSourceWithBlockNames(
	overrides?: Partial<TriggerSourceBlockNames>,
) {
	return triggerSourceWith({
		triggerSourceBlockNames: triggerSourceBlockNames(overrides),
	});
}
export function isTriggerSourceBlockNames(
	node: TriggerSource,
): node is TriggerSourceWith<TriggerSourceBlockNames> {
	return 'triggerSourceBlockNames' in node;
}

export function triggerTargetWithAnimation(
	overrides?: Partial<TriggerTargetAnimation>,
) {
	return triggerTargetWith({
		triggerTargetAnimation: triggerTargetAnimation(overrides),
	});
}
export function isTriggerTargetAnimation(
	node: TriggerTarget,
): node is TriggerTargetWith<TriggerTargetAnimation> {
	return 'triggerTargetAnimation' in node;
}

export function triggerTargetWithSound(
	overrides?: Partial<TriggerTargetSound>,
) {
	return triggerTargetWith({
		triggerTargetSound: triggerTargetSound(overrides),
	});
}
export function isTriggerTargetSound(
	node: TriggerTarget,
): node is TriggerTargetWith<TriggerTargetSound> {
	return 'triggerTargetSound' in node;
}

export function triggerTargetWithGASM(overrides?: Partial<TriggerTargetGASM>) {
	return triggerTargetWith({
		triggerTargetGASM: triggerTargetGASM(overrides),
	});
}
export function isTriggerTargetGASM(
	node: TriggerTarget,
): node is TriggerTargetWith<TriggerTargetGASM> {
	return 'triggerTargetGASM' in node;
}

export function triggerTargetWithLight(
	overrides?: Partial<TriggerTargetLight>,
) {
	return triggerTargetWith({
		triggerTargetLight: triggerTargetLight(overrides),
	});
}
export function isTriggerTargetLight(
	node: TriggerTarget,
): node is TriggerTargetWith<TriggerTargetLight> {
	return 'triggerTargetLight' in node;
}

export function triggerTargetWithSubLevel(
	overrides?: Partial<TriggerTargetSubLevel>,
) {
	return triggerTargetWith({
		triggerTargetSubLevel: triggerTargetSubLevel(overrides),
	});
}
export function isTriggerTargetSubLevel(
	node: TriggerTarget,
): node is TriggerTargetWith<TriggerTargetSubLevel> {
	return 'triggerTargetSubLevel' in node;
}

export function triggerTargetWithAmbience(
	overrides?: Partial<TriggerTargetAmbience>,
) {
	return triggerTargetWith({
		triggerTargetAmbience: triggerTargetAmbience(overrides),
	});
}
export function isTriggerTargetAmbience(
	node: TriggerTarget,
): node is TriggerTargetWith<TriggerTargetAmbience> {
	return 'triggerTargetAmbience' in node;
}

export function levelNodeWithTrigger(overrides?: Partial<LevelNodeTrigger>) {
	return levelNodeWith({
		levelNodeTrigger: levelNodeTrigger(overrides),
	});
}
export function isLevelNodeTrigger(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeTrigger> {
	return 'levelNodeTrigger' in node;
}

export function levelNodeWithSound(overrides?: Partial<LevelNodeSound>) {
	return levelNodeWith({
		levelNodeSound: levelNodeSound(overrides),
	});
}
export function isLevelNodeSound(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeSound> {
	return 'levelNodeSound' in node;
}

export function levelNodeWithGASM(overrides?: Partial<LevelNodeGASM>) {
	return levelNodeWith({
		levelNodeGASM: levelNodeGASM(overrides),
	});
}
export function isLevelNodeGASM(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeGASM> {
	return 'levelNodeGASM' in node;
}

export function levelNodeWithLight(overrides?: Partial<LevelNodeLight>) {
	return levelNodeWith({
		levelNodeLight: levelNodeLight(overrides),
	});
}
export function isLevelNodeLight(
	node: LevelNode,
): node is LevelNodeWith<LevelNodeLight> {
	return 'levelNodeLight' in node;
}
