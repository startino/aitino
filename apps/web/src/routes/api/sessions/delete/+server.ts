import { fail } from '@sveltejs/kit';
import * as db from '$lib/server/db';

export const POST = async ({ request }) => {
	// input and validation
	console.log('session: delete');
	const { sessionId } = (await request.json()) as { sessionId: string };
	if (!sessionId) return fail(400, { detail: 'No session ID provided.' });

	// content
	await db.deleteSession(sessionId);
};
