export function merge<T extends object>(target: T, source: Partial<T>): T {
	for (const key in source) {
		const src = source[key];
		const tgt = target[key];

		if (
			src !== undefined &&
			typeof src === 'object' &&
			!Array.isArray(src)
		) {
			if (!tgt || typeof tgt !== 'object' || Array.isArray(tgt)) {
				target[key] = {} as T[typeof key];
			}
			merge(
				target[key] as T[keyof T] & object,
				src as Partial<T[keyof T]>,
			);
		} else {
			target[key] = src as T[Extract<keyof T, string>];
		}
	}
	return target;
}

type StartingWith<Type, Prefix extends string> = {
	[Key in Extract<keyof Type, `${Prefix}${string}`>]: Type[Key];
};

export type KeyMapping<Type, Key extends string> = StartingWith<
	Required<Type>,
	Key
>;

type Exact<T, U> = [T] extends [U] ? ([U] extends [T] ? true : false) : false;

type MatchesAnyType<Types, K, T extends Types[]> = T extends [
	infer Head,
	...infer Tail,
]
	? Exact<Required<Head>, Required<K>> extends true
		? true
		: Tail extends Types[]
			? MatchesAnyType<Types, K, Tail>
			: false
	: false;

export type PropsStartingWith<T, Prefix extends string> = T[Extract<
	keyof T,
	`${Prefix}${string}`
>];

export type AllKeys<Types> = Types extends unknown ? keyof Types : never;

export type KeysOfType<Type, SubType, Key extends string> = {
	[K in keyof KeyMapping<Type, Key>]: Exact<
		Required<SubType>,
		Required<KeyMapping<Type, Key>[K]>
	> extends true
		? K
		: never;
}[keyof KeyMapping<Type, Key>];

export type TypesExcept<
	Type,
	Key extends string,
	SubTypes,
	Exclude extends SubTypes[],
> = KeyMapping<Type, Key>[keyof {
	[
		L in {
			[K in keyof KeyMapping<Type, Key>]: MatchesAnyType<
				SubTypes,
				KeyMapping<Type, Key>[K],
				Exclude
			> extends true
				? never
				: K;
		}[keyof KeyMapping<Type, Key>]
	]: NonNullable<PropsStartingWith<Type, L>>;
}];
