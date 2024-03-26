import * as db from '$lib/server/db';
import type { SessionLoad } from '$lib/types/loads';
import * as models from '$lib/types/models';
import type { PageServerLoad } from './$types';
import { error, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params, locals: { getSession } }) => {
	const userSession = await getSession();
	if (!userSession) throw error(401, 'You are not logged in. Please log in and try again.');

	// TODO: do this if no slug is provided
	// const session = await db.getRecentSession(userSession.user.id);
	const session = await db.getSession(params.slug);

	if (!session) redirect(303, '/app/session');

	const crew: models.Crew | null = await db.getCrew(session.crew_id);

	if (!crew)
		throw error(
			404,
			'The crew for this session does not exist. Please report this incident. Contact support if the output of this session was important.'
		);

	const data: SessionLoad = {
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
