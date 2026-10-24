export interface BaseInput {
	label?: string;
	text?: string;
}

export type OptionInput = BaseInput & {
	type: 'option';
	options: string[];
};
export type TextareaInput = BaseInput & {
	type: 'textarea';
};
export type RangeInput = BaseInput & {
	type: 'range';
	min: number;
	max: number;
	value: number;
	step?: number;
};
export type CheckboxInput = BaseInput & {
	type: 'checkbox';
	default?: boolean;
};
export type FileInput = BaseInput & {
	type: 'file';
	accept?: string;
	multiple?: boolean;
};

export type SpecificInput =
	OptionInput | TextareaInput | RangeInput | CheckboxInput | FileInput;
export type UnspecifiedInput = BaseInput & {
	type: Exclude<string, Pick<SpecificInput, 'type'>>;
	text?: string;
	accept?: string;
	multiple?: boolean;
};

export type Input = SpecificInput | UnspecifiedInput;
