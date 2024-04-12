import { error, redirect } from '@sveltejs/kit';
import api from '$lib/api';

export const load = async ({ url, locals: { getSession } }) => {
	const userSession = await getSession();

	if (!userSession) throw error(401, 'You are not logged in. Please log in and try again.');

	const sessions = await api.GET('/sessions/', {
		params: {
			query: {
				by_profile: userSession.user.id
			}
		}
	});
	// const sessions: SessionResponse[] = await SessionsService.getSessionsSessionsGet(
	// 	userSession.user.id,
	// 	null
	// ).catch((e: unknown) => {
	// 	console.error(`Error retrieving sessions: ${e}`);
	// 	return [];
	// });

	if (sessions.length > 0 && !url.searchParams.has('debug')) {
		console.log(`Redirecting to session ${sessions[0].id}`);
		redirect(303, `/app/session/${sessions[0].id}`);
	}

	// const crews: CrewResponseModel[] = await CrewsService.getCrewsOfUserCrewsGet(
	// 	userSession.user.id,
	// 	false
	// ).catch((e: unknown) => {
	// 	console.error(`Error retrieving crews: ${e}`);
	// 	return [];
	// });

	const data = {
		profileId: userSession.user.id,
		crews: crews
	};

	return data;
};
