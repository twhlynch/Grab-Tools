import { SERVER_URL } from '@/config';

export async function can_download_level_request(level_id: string) {
	const url = `${SERVER_URL}can_download_level?level_id=${level_id}`;

	try {
		const response = await fetch(url);

		if (response.status !== 200) {
			return null;
		}

		const result = (await response.json()) as {
			allow: boolean | null;
		};

		return result.allow;
	} catch {
		return null;
	}
}
