import { crews } from "$lib/dummy-data/temp-crew";
import * as db from "$lib/server/db";
import type { SessionLoad } from "$lib/types/loads";
import type { Crew, Session } from "$lib/types/models";
import type { PageServerLoad, Actions } from "./$types";
import { error, json} from "@sveltejs/kit";

export const load: PageServerLoad = async ({ cookies, locals: { getSession } }) => {

	const session = await getSession();
	const profileId = session?.user?.id; // TODO: add checks

	const recentSession = await db.getRecentSession(profileId);  

	return {
		recentSession: recentSession,
		recentSessionMessages: recentSession ? db.getMessages(recentSession.id) : [] ,
		allSessions: db.getSessions(profileId),
		recentCrew: await db.getRecentCrew(profileId),
	}
};

export const actions: Actions = {
	"get-messages": async ({ url}) => {
		const sessionId = url.searchParams.get("sessionId");
		if (!sessionId) throw error(400, "This session does not exist. Please reload the page.");
		const messages = await db.getMessages(sessionId);

		return json(messages);
		
	},
	"get-session": async ({url}) => {
		const sessionId = url.searchParams.get("sessionId");
		if (!sessionId) throw error(400, "This session does not exist. Please reload the page.");
		const session: Session | null = await db.getSession(sessionId);
		return json(session);
	},
	rename:  async ({request}) => {
		const { sessionId, newName} = await request.json();
		if (!sessionId) throw error(400, "No session ID provided.");
		if (!newName) throw error(400, "No new name provided.");
		await db.renameSession(sessionId, newName);
		console.log("sessionId", sessionId, "newName", newName);
	},
};
