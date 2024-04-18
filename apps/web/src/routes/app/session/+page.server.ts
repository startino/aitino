import { error, redirect } from '@sveltejs/kit';
import api from '$lib/api';
import type { Session } from '@supabase/supabase-js';

const redirectToSessions = async (userSession: Session) => {
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
				console.error(`Error retrieving sessions: ${e.detail}`);
				return [];
			}
			if (!d) {
				console.error(`No data returned from sessions`);
				return [];
			}
			return d;
		});

	if (sessions[0]) {
		console.log(`Redirecting to session ${sessions[0].id}`);
		redirect(303, `/app/session/${sessions[0].id}`);
	}
};

export const load = async ({ url, locals: { getSession } }) => {
	const userSession = await getSession();

	if (!url.searchParams.has('debug')) {
		await redirectToSessions(userSession);
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
				console.error(`Error retrieving crews: ${e.detail}`);
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
