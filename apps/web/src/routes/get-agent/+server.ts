import { error, json } from '@sveltejs/kit';
import * as db from '$lib/server/db';

// TODO: I wasn't succeeding in calling the "get-agent" action from +page.server.ts
// So I'm calling it from here. If possible, move it back as a named action.
export async function GET({url}) {
    const agentId = url.searchParams.get("agentId");
    if (!agentId) throw error(400, "No agent ID provided.");
    const agent = await db.getAgent(agentId);
    console.log("agent got. returning: ", agent)
	return json({agent: agent});
}