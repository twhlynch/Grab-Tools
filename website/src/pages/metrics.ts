export const metricKeys = [
	'level_records',
	'level_finishes',
	'challenge_finishes',
	'challenge_records',
	'featured_records',
	'sole_finishes',
	'challenge_created',
	'unbeaten_created',
	'hardest_created',
	'hardest_created_placement',
] as const;

export type MetricKey = (typeof metricKeys)[number];

export type Metric = {
	score: number;
	maps: number;
	username: string;
	username_priority: number;
	positions: Record<MetricKey, number>;
	raw: Record<MetricKey, number>;
} & Record<MetricKey, number>;

export function metricDict<T>(value: T): Record<MetricKey, T> {
	return Object.fromEntries(metricKeys.map((key) => [key, value])) as Record<
		MetricKey,
		T
	>;
}
