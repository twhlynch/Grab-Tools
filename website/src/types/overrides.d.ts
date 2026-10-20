import { Reactive } from 'vue';
import { Root } from './levelNodes';

type Severity = 'message' | 'info' | 'warn' | 'warning' | 'err' | 'error';

declare global {
	interface Window {
		dataLayer?: IArguments[];
		_root?: Root;
		toast: (
			message: string | Error,
			severity?: Severity,
			persistent?: boolean,
		) => void | {
			remove: () => void;
			message: Reactive<{
				value: string;
				error: Error | null;
				id: string;
				severity: Severity;
			}>;
		};
	}

	interface MediaStreamTrackProcessor {
		readable: ReadableStream<VideoFrame>;
	}

	var MediaStreamTrackProcessor: {
		new (init: { track: MediaStreamTrack }): MediaStreamTrackProcessor;
		readonly prototype: MediaStreamTrackProcessor;
	};

	interface HTMLVideoElement {
		captureStream: () => MediaStream;
	}
}
