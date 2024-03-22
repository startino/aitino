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
		crew: crew, // TODO: this will be obsolete when library feature is done. Instead a crew will be selected manually.
		reply: ''
	};

	return data;
};

export const actions: Actions = {
	'get-messages': async ({ url }) => {
		const sessionId = url.searchParams.get('sessionId');
		if (!sessionId) throw error(400, 'No session ID provided.');
		const messages = await db.getMessages(sessionId);

		return json(messages);
	},
	'get-session': async ({ url }) => {
		console.log('GET SESSION');
		const sessionId = url.searchParams.get('sessionId');
		if (!sessionId) throw error(400, 'No session ID provided');
		const session: models.Session | null = await db.getSession(sessionId);
		if (!session) throw error(400, 'This session does not exist. Please reload the page.');
		console.log('session:', session);
		return json({ session });
	},
	'get-agent': async ({ url }) => {
		// TODO: this is not being called. the route /api/get-agent is being used.
		// I wasn't able to call this from Message.svelte in fetch.
		// So it is temporarily being called from /api/get-agent. This should be used instead if possible.
		console.log('getting agent');
		const agentId = url.searchParams.get('agentId');
		if (!agentId) throw error(400, 'No agent ID provided.');
		const agent = await db.getAgent(agentId);
		console.log('agent: ', agent);
		return json(agent);
	},
	rename: async ({ request }) => {
		const { sessionId, newTitle } = await request.json();
		if (!sessionId) throw error(400, 'No session ID provided.');
		if (newTitle == '') throw error(400, 'No new name provided.');
		await db.renameSession(sessionId, newTitle);
		console.log('sessionId', sessionId, 'newName', newTitle);
	},
	delete: async ({ request }) => {
		const { sessionId } = await request.json();
		if (!sessionId) throw error(400, 'No session ID provided.');
		await db.deleteSession(sessionId);
	},
	'set-status': async ({ request }) => {
		const { sessionId, status } = await request.json();
		if (!sessionId) throw error(400, 'No session ID provided.');
		if (!status) throw error(400, 'No status provided.');
		await db.setSessionStatus(sessionId, status);
	}
};
