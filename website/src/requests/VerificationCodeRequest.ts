import { SERVER_URL } from '@/config';
import { handle_auth_error } from '@/requests/RequestUtils';
import { useUserStore } from '@/stores/user';

export async function verification_code_request() {
	const userStore = useUserStore();
	const url = `${SERVER_URL}get_verification_code?access_token=${userStore.access_token}`;

	try {
		const response = await fetch(url);

		if (!response.ok) {
			const text = await response.text();
			if (handle_auth_error(response)) return null;
			window.toast(`Error: ${text}`, 'error');
			return null;
		}

		const json = (await response.json()) as { code: string };
		return json.code;
	} catch {
		window.toast(`Error: Failed to get code`, 'error');
		return null;
	}
}
