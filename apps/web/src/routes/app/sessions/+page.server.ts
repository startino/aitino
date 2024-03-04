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
			const messages = await db.getMessages(sessionId);
		
			return json(messages);
		
	},
	"get-session": async ({url}) => {
		const sessionId = url.searchParams.get("sessionId");
		const session: SessionLoad = await db.getSession(sessionId);
		return json(session);
	}
};
