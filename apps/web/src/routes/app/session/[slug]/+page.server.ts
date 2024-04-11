import {
	AgentsService,
	CrewsService,
	MessagesService,
	SessionsService
} from '$lib/client/index.js';
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

	return {
		profileId: userSession.user.id,
		session: session,
		sessions: await SessionsService.getSessionsSessionsGet(userSession.user.id, null).catch(
			(e: unknown) => {
				console.error(`Error retrieving sessions: ${e}`);
				return [];
			}
		),
		crew: crew,
		crews: await CrewsService.getCrewsOfUserCrewsGet(userSession.user.id, false).catch(
			(e: unknown) => {
				console.error(`Error retrieving crews: ${e}`);
				return [];
			}
		),
		// TODO: Why can id be null here? Verify if we can ensure it's always set in the api's return.
		messages: session.id ? MessagesService.getMessagesSessionsMessagesGet(session.id) : [],
		agents: await AgentsService.getAgentsFromCrewAgentsByCrewGet(crew.id).catch((e: unknown) => {
			console.error(`Error retrieving agents: ${e}`);
			return [];
		})
	};
};
