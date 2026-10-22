declare module 'jsfft' {
	export interface ComplexValue {
		real: number;
		imag: number;
	}

	export type ComplexMapper = (
		value: ComplexValue,
		index: number,
		length: number,
	) => void;

	export class ComplexArray {
		constructor(
			other: ComplexArray | number | ArrayLike<number>,
			arrayType?: Float32ArrayConstructor,
		);

		ArrayType: Float32ArrayConstructor;
		real: Float32Array;
		imag: Float32Array;
		length: number;

		toString(): string;

		forEach(iterator: ComplexMapper): void;

		map(mapper: ComplexMapper): this;

		conjugate(): ComplexArray;

		magnitude(): Float32Array;

		FFT(): ComplexArray;

		InvFFT(): ComplexArray;

		frequencyMap(filterer: ComplexMapper): ComplexArray;
	}

	export function FFT(
		input: ComplexArray | number | ArrayLike<number>,
	): ComplexArray;

	export function InvFFT(
		input: ComplexArray | number | ArrayLike<number>,
	): ComplexArray;

	export function frequencyMap(
		input: ComplexArray | number | ArrayLike<number>,
		filterer: ComplexMapper,
	): ComplexArray;

	export function FFTImageDataRGBA(
		data: Uint8ClampedArray | Uint8Array,
		nx: number,
		ny: number,
	): ComplexArray;
}
