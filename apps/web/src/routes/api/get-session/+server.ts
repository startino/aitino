import { error, json } from '@sveltejs/kit';
import * as db from '$lib/server/db';
import type { Session } from '$lib/types/models';

// TODO: I couldn't call this action from +page.server.ts
// So I'm calling it from here. If possible, move it back as a named action.
export async function GET({url}) {
    const sessionId = url.searchParams.get("sessionId");
    if (!sessionId) throw error(400, "This session does not exist. Please reload the page.");
    const session: Session | null = await db.getSession(sessionId);
    return json({session});
}