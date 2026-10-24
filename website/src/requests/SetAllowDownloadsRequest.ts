import { SERVER_URL } from '@/config';
import { handle_auth_error } from '@/requests/RequestUtils';
import { useUserStore } from '@/stores/user';

export async function set_allow_downloads_request(
	level_id: string | null | undefined,
	user_id: string | null | undefined,
	allow: boolean | null,
) {
	const user = useUserStore();

	level_id ??= '';
	user_id ??= ''; // '' is falsy
	const url = `${SERVER_URL}set_allow_downloads?level_id=${level_id}&user_id=${user_id}&allow=${allow}&access_token=${user.access_token}`;

	try {
		const response = await fetch(url);

		if (!response.ok) {
			handle_auth_error(response);
			return null;
		}

		const success = await response.text();
		return success === 'Success';
	} catch {
		return null;
	}
}
