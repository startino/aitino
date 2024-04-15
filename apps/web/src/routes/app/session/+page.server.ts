import { error, redirect } from '@sveltejs/kit';
import api from '$lib/api';

export const load = async ({ url, locals: { getSession } }) => {
	const userSession = await getSession();

	if (!userSession) throw error(401, 'You are not logged in. Please log in and try again.');

	const sessions = await api
		.GET('/sessions/', {
			params: {
				query: {
					profile_id: userSession.user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving sessions: ${e}`);
				return [];
			}
			if (!d) {
				console.error(`No data returned from sessions`);
				return [];
			}
			return d;
		});

	if (sessions[0] && !url.searchParams.has('debug')) {
		console.log(`Redirecting to session ${sessions[0].id}`);
		redirect(303, `/app/session/${sessions[0].id}`);
	}

	const crews = await api
		.GET('/crews/', {
			params: {
				query: {
					profile_id: userSession.user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving crews: ${e}`);
				return [];
			}
			if (!d) {
				console.error(`No data returned from crews`);
				return [];
			}
			return d;
		});

	return {
		profileId: userSession.user.id,
		crews: crews
	};
};
