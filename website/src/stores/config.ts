import { defineStore } from 'pinia';

export const useConfigStore = defineStore('config', {
	state: (): {
		editor_config: object | undefined;
		default_level: string | undefined;
		dark_mode: boolean;
		vim_enabled: boolean;
		default_gasm: string;
		active_gasm_tab: number;
	} => ({
		editor_config: undefined,
		default_level: undefined,
		dark_mode: false,
		vim_enabled: false,
		default_gasm: '',
		active_gasm_tab: 0,
	}),
	actions: {
		set_dark_mode(value: boolean) {
			this.dark_mode = value;
		},
		set_vim(value: boolean) {
			this.vim_enabled = value;
		},
		set_default_gasm(value: string) {
			this.default_gasm = value;
		},
		set_active_gasm_tab(value: number) {
			this.active_gasm_tab = value;
		},
	},
	persist: true,
});
