import * as db from '$lib/server/db';
import type { SessionsLoad } from '$lib/types/loads';
import * as models from '$lib/types/models';
import type { PageServerLoad, Actions } from './$types';
import { error, json } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ url, cookies, locals: { getSession } }) => {
	const session = await getSession();
	if (!session) throw error(401, 'You are not logged in. Please log in and try again.');

	const recentSession = await db.getRecentSession(session.user.id);
	console.log('recentSession:', recentSession);
	const crew: models.Crew | null = recentSession
		? await db.getCrew(recentSession.crew_id)
		: await db.getRecentCrew(session.user.id);
	console.log('crew:', crew);

	const data: SessionsLoad = {
		profileId: session.user.id,
		session: recentSession,
		sessions: await db.getSessions(session.user.id),
		messages: recentSession ? await db.getMessages(recentSession.id) : ([] as models.Message[]),
		crew: crew,
		reply: ''
	};

	return data;
};

export const actions: Actions = {
	getmessages: async ({ request }) => {
		// input and validation
		console.log('getmessages');
		const { sessionId } = (await request.json()) as { sessionId: string };
		if (!sessionId) throw error(400, 'No session ID provided.');

		// content
		const messages = await db.getMessages(sessionId);

		return json(messages);
	},
	getsession: async ({ request }) => {
		// input and validation
		console.log('getsession');
		const { sessionId } = (await request.json()) as { sessionId: string };
		if (!sessionId) throw error(400, 'No session ID provided');
		const session: models.Session | null = await db.getSession(sessionId);
		if (!session) throw error(400, 'This session does not exist. Please reload the page.');

		// content
		console.log('session:', session);
		return json({ session });
	},
	getagent: async ({ request }) => {
		// input and validation
		console.log('getagent');
		const { agentId } = (await request.json()) as { agentId: string };
		if (!agentId) throw error(400, 'No agent ID provided.');

		// content
		const agent = await db.getAgent(agentId);
		return json({ agent });
	},
	rename: async ({ request }) => {
		// input and validation
		console.log('rename');
		const { sessionId, newTitle } = (await request.json()) as {
			sessionId: string;
			newTitle: string;
		};
		if (!sessionId) throw error(400, 'No session ID provided.');
		if (newTitle == '') throw error(400, 'No new name provided.');

		// content
		await db.renameSession(sessionId, newTitle);
	},
	delete: async ({ request }) => {
		// input and validation
		console.log('delete');
		const { sessionId } = (await request.json()) as { sessionId: string };
		if (!sessionId) throw error(400, 'No session ID provided.');

		// content
		await db.deleteSession(sessionId);
	},
	setstatus: async ({ request }) => {
		// input and validation
		console.log('setstatus');
		const { sessionId, status } = (await request.json()) as {
			sessionId: string;
			status: string;
		};
		if (!sessionId) throw error(400, 'No session ID provided.');
		if (!status) throw error(400, 'No status provided.');

		// content
		await db.setSessionStatus(sessionId, status);
	}
};
