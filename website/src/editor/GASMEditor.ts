import { create_connection } from '@/common/connections';
import { compile_gasm } from '@/editor/AssemblyConversion';
import build_editor from '@/editor/EditorSetup';
import {
	gasmCompletion,
	update_json_completions,
} from '@/editor/GASMCompletion';
import { gasmDiagnostics } from '@/editor/GASMDiagnostics';
import { gasm } from '@/editor/GASMDSL';
import { levelNodeWithGASM } from '@/generated/nodes';
import { useConfigStore } from '@/stores/config';
import { redo, undo } from '@codemirror/commands';
import { foldGutter } from '@codemirror/language';
import { highlightSelectionMatches, searchKeymap } from '@codemirror/search';
import { EditorSelection, EditorState } from '@codemirror/state';
import { EditorView, ViewUpdate } from '@codemirror/view';
import { vim } from '@replit/codemirror-vim';
import { basicSetup } from 'codemirror';

export interface BaseEditor {
	view: EditorView;

	get(): string;
	set(text: string): void;
	compile(): string | undefined;

	focus(): void;
	undo(): void;
	redo(): void;
	copy(): Promise<void>;
	paste(): Promise<void>;
}

type ChangeCallback = (update: ViewUpdate) => void;

export type EditorConstructor = new (
	domElement: HTMLElement,
	changed?: ChangeCallback,
) => BaseEditor;

export class OutputEditor implements BaseEditor {
	static title = 'Output';
	view: EditorView;

	constructor(domElement: HTMLElement, changed?: ChangeCallback) {
		this.view = build_editor(
			domElement,
			'',
			gasm,
			[
				foldGutter(),
				highlightSelectionMatches(),
				...(useConfigStore().vim_enabled ? [vim()] : []),
				basicSetup,
				EditorState.readOnly.of(true),
			],
			[...searchKeymap],
			changed,
		);
	}

	get() {
		return this.view.state.doc.toString();
	}

	set(insert: string) {
		const to = this.view.state.doc.length;
		const changes = { from: 0, to, insert };
		this.view.dispatch({ changes });
	}

	compile() {
		return this.get();
	}

	focus() {
		this.view.focus();
		this.view.dispatch({
			selection: EditorSelection.cursor(this.view.state.doc.length),
			scrollIntoView: true,
		});
	}

	undo() {
		//
	}

	redo() {
		//
	}

	async copy() {
		try {
			const text = this.get();
			await navigator.clipboard.writeText(text);
		} catch (e) {
			if (e instanceof Error) {
				window.toast(e, 'error');
			}
		}
	}

	async paste() {
		//
	}
}

export class GASMEditor implements BaseEditor {
	static title = 'GASM Editor';
	view: EditorView;

	constructor(domElement: HTMLElement, changed?: ChangeCallback) {
		this.view = build_editor(
			domElement,
			useConfigStore().default_gasm,
			gasm,
			[
				foldGutter(),
				highlightSelectionMatches(),
				...(useConfigStore().vim_enabled ? [vim()] : []),
				basicSetup,
				...gasmCompletion(),
				gasmDiagnostics,
			],
			[...searchKeymap],
			(update: ViewUpdate) => {
				this.update(update);
				changed?.(update);
			},
		);

		// for autocompletion
		const node = levelNodeWithGASM();
		create_connection(node, undefined, 0, 'player', undefined);
		create_connection(node, undefined, 1, 'sign', 'Obj');
		create_connection(node, undefined, 1, 'position', 'Obj');
		create_connection(node, undefined, 1, 'rotation', 'Obj');
		create_connection(node, undefined, 1, 'scale', 'Obj');
		create_connection(node, undefined, 1, 'triggerActive', 'Obj');
		create_connection(node, undefined, 1, 'color', 'Obj');
		create_connection(node, undefined, 1, 'scale', 'Obj');
		create_connection(node, undefined, 1, 'physics', 'Obj');
		create_connection(node, undefined, 1, 'light', 'Obj');
		create_connection(node, undefined, 0, 'lobbyVariables', undefined);
		create_connection(node, undefined, 0, 'playerVariables', undefined);
		update_json_completions(node);
	}

	update(update: ViewUpdate) {
		if (!update.docChanged) return;

		const text = update.state.doc.toString();
		useConfigStore().set_default_gasm(text);
	}

	get() {
		return this.view.state.doc.toString();
	}

	set(insert: string) {
		const to = this.view.state.doc.length;
		const changes = { from: 0, to, insert };
		this.view.dispatch({ changes });
	}

	compile() {
		try {
			const source = this.get();
			return compile_gasm(source).join('\n');
		} catch (e) {
			if (e instanceof Error) {
				console.log(e.message);
			}
		}
	}

	focus() {
		this.view.focus();
		this.view.dispatch({
			selection: EditorSelection.cursor(this.view.state.doc.length),
			scrollIntoView: true,
		});
	}

	undo() {
		undo(this.view);
	}

	redo() {
		redo(this.view);
	}

	async copy() {
		try {
			const text = this.get();
			await navigator.clipboard.writeText(text);
		} catch (e) {
			if (e instanceof Error) {
				window.toast(e, 'error');
			}
		}
	}

	async paste() {
		try {
			const text = await navigator.clipboard.readText();
			this.set(text);
		} catch (e) {
			if (e instanceof Error) {
				window.toast(e, 'error');
			}
		}
	}
}
