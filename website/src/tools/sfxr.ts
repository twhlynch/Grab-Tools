import { SoundGeneratorParameters } from '@grab-tools/lib/generated/proto';
import { sfxr } from 'jsfxr';

// missing some keys:
// p_lpf_ramp p_lpf_resonance p_hpf_ramp
// reverbDelay reverbDecayFactor

const PARAM_MAP: Record<string, string> = {
	waveType: 'wave_type',
	envelopeAttack: 'p_env_attack',
	envelopeSustain: 'p_env_sustain',
	envelopePunch: 'p_env_punch',
	envelopeRelease: 'p_env_decay',
	frequencyBase: 'p_base_freq',
	frequencyLimit: 'p_freq_limit',
	frequencyRamp: 'p_freq_ramp',
	frequencyDeltaRamp: 'p_freq_dramp',
	vibratoStrength: 'p_vib_strength',
	vibratoSpeed: 'p_vib_speed',
	pitchJumpMod: 'p_arp_mod',
	pitchJumpSpeed: 'p_arp_speed',
	dutyCycle: 'p_duty',
	dutyCycleRamp: 'p_duty_ramp',
	repeatSpeed: 'p_repeat_speed',
	flangerFrequency: 'p_pha_offset',
	flangerDepth: 'p_pha_ramp',
	lowPassFilterFrequency: 'p_lpf_freq',
	highPassFilterFrequency: 'p_hpf_freq',
};

const CONVERSION_MAP: Record<string, (v: number) => number> = {
	p_env_attack: (v) => clamp01(Math.sqrt(v * 0.441)),
	p_env_sustain: (v) => clamp01(Math.sqrt(v * 0.441)),
	p_env_punch: (v) => clamp01(v * 0.5),
	p_env_decay: (v) => clamp01(Math.sqrt(v * 0.441)),
	p_base_freq: (v) => clamp01(Math.sqrt(v / 3528)),
	p_freq_limit: (v) => clamp01(Math.sqrt(v / 3528)),
	p_freq_ramp: (v) => sign(v) * clamp01(Math.cbrt(Math.abs(v) / 100)),
	p_freq_dramp: (v) => sign(v) * clamp01(Math.cbrt(Math.abs(v) / 100)),
	p_vib_strength: (v) => clamp01(v / 0.5),
	p_vib_speed: (v) => clamp01(Math.sqrt(v / 69)),
	p_arp_mod: (v) =>
		v >= 1
			? clamp11(Math.sqrt((v - 1) / (0.9 * v)))
			: clamp11(-Math.sqrt((1 - v) / (10 * Math.max(v, 0.001)))),
	p_arp_speed: (v) => clamp01(Math.sqrt(v / 0.5)),
	p_duty: (v) => clamp11(1 - v * 2),
	p_duty_ramp: (v) => clamp11(v),
	p_repeat_speed: (v) => clamp01(Math.sqrt(v / 0.5)),
	p_pha_offset: (v) => clamp01(Math.sqrt(v / 100)),
	p_pha_ramp: (v) => clamp01(v * 2),
	p_lpf_freq: (v) => clamp01(Math.sqrt(v / 16000)),
	p_hpf_freq: (v) => clamp01(Math.sqrt(v / 16000)),
};

const clamp = (v: number, min: number, max: number) => {
	return Math.min(max, Math.max(min, v));
};
const clamp01 = (v: number) => {
	return clamp(v, 0, 1);
};
const clamp11 = (v: number) => {
	return clamp(v, -1, 1);
};
const sign = (v: number) => {
	return v >= 0 ? 1 : -1;
};

export function play_sound(params: SoundGeneratorParameters) {
	// prettier-ignore
	const sfxr_params: Record<string, number | boolean> = {
		oldParams: true,
		wave_type: 0,
		p_env_attack: 0, p_env_sustain: 0, p_env_punch: 0, p_env_decay: 0,
		p_base_freq: 0, p_freq_limit: 0, p_freq_ramp: 0, p_freq_dramp: 0,
		p_vib_strength: 0, p_vib_speed: 0,
		p_arp_mod: 0, p_arp_speed: 0,
		p_duty: 0, p_duty_ramp: 0,
		p_repeat_speed: 0,
		p_pha_offset: 0, p_pha_ramp: 0,
		p_lpf_freq: 0, p_lpf_ramp: 0, p_lpf_resonance: 0,
		p_hpf_freq: 0, p_hpf_ramp: 0,
		sound_vol: 0.5,
		sample_rate: 44100,
		sample_size: 8,
	};

	for (const [key, value] of Object.entries(params) as [string, number][]) {
		const sfxr_key = PARAM_MAP[key];
		if (sfxr_key)
			sfxr_params[sfxr_key] = CONVERSION_MAP[sfxr_key]?.(value) ?? value;
	}

	sfxr.play(sfxr_params);
}
