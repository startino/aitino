import type { UUID } from '$lib/types';
import * as models from '$lib/types/models';
import { PUBLIC_API_URL } from '$env/static/public';

export const upsertSession = async (sessionId: UUID, content: object): Promise<boolean> => {
	console.log('upsertSession', sessionId, content);
	const success: boolean = await fetch(
		`${PUBLIC_API_URL}/sessions/upsert?session_id=${sessionId}`,
		{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(content)
		}
	)
		.then(async (response) => {
			if (!response.ok) {
				console.error(`Failed to upsert session. Bad response`, response, await response.json());
				return false;
			}
			return true;
		})
		.catch((error) => {
			console.error('upsertSession: error', error);
			return false;
		});

	return success;
};

export const startSession = async (
	profileId: UUID,
	crewId: UUID,
	title: string
): Promise<models.Session | false> => {
	console.log('startSession', profileId, crewId, title);
	const response: models.Session | false = await fetch(
		`${PUBLIC_API_URL}/sessions/run?id=${crewId}&profile_id=${profileId}&session_title=${encodeURIComponent(title)}`
	)
		.then(async (response) => {
			if (!response.ok) {
				console.error(`Failed to upsert session. Bad response`, response, await response.json());
				return false;
			}
			const {
				data: { session }
			} = (await response.json()) as { data: { session: models.Session } };
			return session;
		})
		.catch((error) => {
			console.error(`startSession: error`, error);
			return false;
		});

	return response;
};

export const deleteSession = async (sessionId: UUID): Promise<boolean> => {
	console.log('deleteSession', sessionId);
	const success: boolean = await fetch(`${PUBLIC_API_URL}/sessions/delete`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ session_id: sessionId })
	})
		.then(async (response) => {
			if (!response.ok) {
				console.error(`Failed to upsert session. Bad response`, response, await response.json());
				return false;
			}
			return true;
		})
		.catch((error) => {
			console.error(`deleteSession: error`, error);
			return false;
		});
	return success;
};
