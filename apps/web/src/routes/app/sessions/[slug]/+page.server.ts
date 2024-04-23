import { error, redirect } from '@sveltejs/kit';
import api from '$lib/api';

export const load = async ({ params, locals: { getSession } }) => {
	const userSession = await getSession();

	const session = await api
		.GET('/sessions/{session_id}', {
			params: {
				path: {
					session_id: params.slug
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving sessions: ${e.detail}`);
				throw redirect(303, '/app/sessions');
			}
			if (!d) {
				console.error(`No data returned from sessions`);
				throw redirect(303, '/app/sessions');
			}
			return d;
		});

	// TODO: Handle crew not found better.
	// If the crew is not found, then it is very likely that the user
	// managed to delete their crew while the crew still had sessions. This
	// scenario needs to be discussed so we can decide how to handle it. Likely
	// we will want to completely prevent deletion of crews with active sessions
	// or use some sort of cascade delete behind very strong confirmation dialogs.
	const crew = await api
		.GET('/crews/{crew_id}', {
			params: {
				path: {
					crew_id: session.crew_id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving crew: ${e.detail}`);
				throw error(
					500,
					`Error Retrieving Crew. Contact support if the output of this session was important. Please report this incident to the dev team with the following information: ${e.detail}`
				);
			}
			if (!d) {
				console.error(`Crew ${session.crew_id} not found`);
				throw error(
					404,
					`Crew not found. Contact support if the output of this session was important.`
				);
			}
			return d;
		});

	return {
		profileId: userSession.user.id,
		session: session,
		sessions: await api
			.GET('/sessions/', {
				params: {
					query: {
						profile_id: userSession.user.id
					}
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error retrieving sessions: ${e.detail}`);
					return [];
				}
				if (!d) {
					console.error(`No data returned from sessions`);
					return [];
				}
				return d;
			}),
		crew: crew,
		crews: await api
			.GET('/crews/', {
				params: {
					query: {
						profile_id: userSession.user.id
					}
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error retrieving crews: ${e.detail}`);
					return [];
				}
				if (!d) {
					console.error(`No data returned from crews`);
					return [];
				}
				return d;
			}),
		messages: [],
		agents: await api
			.GET('/agents/', {
				params: {
					query: {
						crew_id: userSession.user.id
					}
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error retrieving agents: ${e.detail}`);
					return [];
				}
				if (!d) {
					console.error(`No data returned from agents`);
					return [];
				}
				return d;
			})
	};
};
