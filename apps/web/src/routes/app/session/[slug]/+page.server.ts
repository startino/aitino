import { CrewsService, SessionsService } from '$lib/client/index.js';
import * as db from '$lib/server/db';
import { error, redirect } from '@sveltejs/kit';

export const load = async ({ params, locals: { getSession } }) => {
	const userSession = await getSession();
	if (!userSession) throw error(401, 'You are not logged in. Please log in and try again.');

	const session = await SessionsService.getSessionsSessionsGet(null, params.slug)
		.then((sessions) => {
			if (sessions.length === 0) {
				console.error(`Session ${params.slug} not found`);
				throw redirect(303, '/app/session');
			}
			return sessions[0];
		})
		.catch((e: unknown) => {
			console.error(`Error retrieving session: ${e}`);
			throw redirect(303, '/app/session');
		});

	// TODO: Handle crew not found better.
	// If the crew is not found, then it is very likely that the user
	// managed to delete their crew while the crew still had sessions. This
	// scenario needs to be discussed so we can decide how to handle it. Likely
	// we will want to completely prevent deletion of crews with active sessions
	// or use some sort of cascade delete behind very strong confirmation dialogs.
	const crew = await CrewsService.getCrewCrewsCrewIdGet(session.crew_id)
		.then((crew) => {
			if (!crew) {
				console.error(`Crew ${session.crew_id} not found`);
				throw error(
					404,
					`Crew not found. Contact support if the output of this session was important. `
				);
			}
			return crew;
		})
		.catch((e: unknown) => {
			console.error(`Error retrieving crew: ${e}`);
			throw error(
				500,
				`Error Retrieving Crew. Contact support if the output of this session was important. Please report this incident to the dev team with the following information: ${e}`
			);
		});

	const data = {
		profileId: userSession.user.id,
		session: session,
		sessions: await db.getSessions(userSession.user.id),
		crew: crew,
		crews: await db.getCrews(userSession.user.id),
		messages: session ? await db.getMessages(session.id) : ([] as models.Message[]),
		agents: await db.getAgents(userSession.user.id)
	};

	return data;
};
