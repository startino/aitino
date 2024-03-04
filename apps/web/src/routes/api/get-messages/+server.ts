import { json } from '@sveltejs/kit';
import * as db from '$lib/server/db';

export async function GET({url}) {
    const sessionId = url.searchParams.get("sessionId");
    const messages = await db.getMessages(sessionId);

	return json(messages);
}