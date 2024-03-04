import { crews } from "$lib/dummy-data/temp-crew";
import * as db from "$lib/server/db";
import type { SessionLoad } from "$lib/types/loads";
import type { Crew, Session } from "$lib/types/models";
import type { PageServerLoad, Actions } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ cookies, locals: { getSession } }) => {

	const session = await getSession();
	const profileId = session?.user?.id; // TODO: add checks

	const recentSession = await db.getRecentSession(profileId);  

	const recentSessionLoad: SessionLoad = {
		profileId,
		crewId: null,
		session: recentSession, // TODO: do not await
		messages: [],
		reply: "",

}

	return {
		recentSession: recentSessionLoad, 
		allSessions: db.getSessions(profileId),
		recentCrew: await db.getRecentCrew(profileId),
	}
};

export const actions: Actions = {
	// create: async ({ request }) => {
	// 	const data = await request.formData();
	// 	db.createTodo(cookies.get('userid'), data.get('description'));
	// },
	//
	// delete: async ({ request }) => {
	// 	const data = await request.formData();
	// 	db.deleteTodo(cookies.get('userid'), data.get('id'));
	// }
};
