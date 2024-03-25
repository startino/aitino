import { fail } from '@sveltejs/kit';
import * as db from '$lib/server/db';

export const POST = async ({ request }) => {
	// input and validation
	console.log('session: update');
	const { sessionId, content } = (await request.json()) as {
		sessionId: string;
		content: object;
	};
	if (!sessionId) return fail(400, { detail: 'No session ID provided.' });
	if (!content) return fail(400, { detail: 'No content.' });

	// content
	await db.updateSession(sessionId, content);
};
