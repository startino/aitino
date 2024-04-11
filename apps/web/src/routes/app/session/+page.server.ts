import {
	CrewsService,
	SessionsService,
	type CrewResponseModel,
	type SessionResponse
} from '$lib/client';
import { error, redirect } from '@sveltejs/kit';

export const load = async ({ url, locals: { getSession } }) => {
	const userSession = await getSession();

	if (!userSession) throw error(401, 'You are not logged in. Please log in and try again.');

	const sessions: SessionResponse[] = await SessionsService.getSessionsSessionsGet(
		userSession.user.id,
		null
	).catch((e: unknown) => {
		console.error(`Error retrieving sessions: ${e}`);
		return [];
	});

	if (sessions.length > 0 && !url.searchParams.has('debug')) {
		console.log(`Redirecting to session ${sessions.length}`);
		redirect(303, `/app/session/${sessions[0].id}`);
	}

	const crews: CrewResponseModel[] = await CrewsService.getCrewsOfUserCrewsGet(
		userSession.user.id,
		false
	).catch((e: unknown) => {
		console.error(`Error retrieving crews: ${e}`);
		return [];
	});

	const data = {
		profileId: userSession.user.id,
		crews: crews
	};

	return data;
};
