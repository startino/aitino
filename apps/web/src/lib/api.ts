import type { UUID } from '$lib/types';
import * as models from '$lib/types/models';
import { PUBLIC_API_URL } from '$env/static/public';

export async function renameSessiojjjjj

export async function startSession(profileId: UUID, crewId: UUID, title: string) {
	const session = await fetch(`${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${profileId}`)
		.then((response) => {
			if (response.status === 200) {
				return response.json() as any;
			} else {
				throw new Error('Failed to start new session. bad respose: ' + response);
			}
		})
		.then((response) => {
			return response.data.session as models.Session;
		})
		.catch((error) => {
			console.error('Failed to start new session. error', error);
			return null;
		});

	return session ? session.id : null;
}

