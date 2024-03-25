import * as db from '$lib/server/db';
import type { SessionLoad } from '$lib/types/loads';
import * as models from '$lib/types/models';
import type { PageServerLoad, Actions } from './$types';
import { fail, error, json, redirect } from '@sveltejs/kit';

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

export const actions: Actions = {
	getmessages: async ({ request }) => {
		// input and validation
		console.log('getmessages');
		const { sessionId } = (await request.json()) as { sessionId: string };
		if (!sessionId) return fail(400, { detail: 'No session ID provided.' });

		// content
		const messages = await db.getMessages(sessionId);

		return json(messages);
	},
	getsession: async ({ request }) => {
		// input and validation
		console.log('getsession');
		const { sessionId } = (await request.json()) as { sessionId: string };
		if (!sessionId) return fail(400, { detail: 'No session ID provided' });

		// content
		const session: models.Session | null = await db.getSession(sessionId);

		if (!session)
			return fail(404, { detail: 'This session does not exist. Please reload the page.' });

		console.log('session: ', session);
		return json({ session });
	},
	getagent: async ({ cookies, request, url }) => {
		// input and validation
		console.log('session: getagent');
		const { agentId } = (await request.json()) as { agentId: string };
		if (!agentId) return fail(400, { detail: 'No agent ID provided.' });

		// content
		const agent = await db.getAgent(agentId);
	},
	rename: async ({ request }) => {
		// input and validation
		console.log('session: rename');
		const { sessionId, newTitle } = (await request.json()) as {
			sessionId: string;
			newTitle: string;
		};
		if (!sessionId) return fail(400, { detail: 'No session ID provided.' });
		if (newTitle == '') return fail(400, { detail: 'No new name provided.' });

		// content
		await db.renameSession(sessionId, newTitle);
	},
	delete: async ({ request }) => {
		// input and validation
		console.log('session: delete');
		const { sessionId } = (await request.json()) as { sessionId: string };
		if (!sessionId) return fail(400, { detail: 'No session ID provided.' });

		// content
		await db.deleteSession(sessionId);
	},
	setstatus: async ({ request }) => {
		// input and validation
		console.log('session: setstatus');
		const { sessionId, status } = (await request.json()) as {
			sessionId: string;
			status: string;
		};
		if (!sessionId) return fail(400, { detail: 'No session ID provided.' });
		if (!status) return fail(400, { detail: 'No status provided.' });

		// content
		await db.setSessionStatus(sessionId, status);
	}
};
