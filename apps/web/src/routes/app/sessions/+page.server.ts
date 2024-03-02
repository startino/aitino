import * as db from "$lib/server/db";
import type { SessionLoad } from "$lib/types/loads";
import type { Crew, Session } from "$lib/types/models";
import type { PageServerLoad, Actions } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({ cookies }) => {
	// BEGIN TEMP FORCE PROFILE
	const profileId = "edb9a148-a8fc-48bd-beb9-4bf5de602b78"; //cookies.get("profileId");
	const expirationDate = new Date();
	expirationDate.setMonth(expirationDate.getMonth() + 1);
	cookies.set("profileId", profileId, {
		path: "/",
		httpOnly: true,
		sameSite: "strict",
		secure: process.env.NODE_ENV === "production",
		expires: expirationDate
	});
	// END TEMP FORCE PROFILE

	if (!profileId) {
		throw error(401, "Unauthorized");
	}

	cookies.set("profileId", profileId, {
		path: "/",
		httpOnly: true,
		sameSite: "strict",
		secure: process.env.NODE_ENV === "production",
		expires: expirationDate
	});

	const data: SessionLoad = {
		profileId: profileId,
		crewId: null,
		session: null,
		messages: [],
		reply: ""
	};

	const crews: Crew[] = await db.getCrews(profileId);
	if (crews.length !== 0) {
		data.crewId = crews[0].id;

		const sessions: Session[] = await db.getSessions(data.profileId, data.crewId);
		if (sessions.length !== 0) {
			data.session = sessions[0];

			data.messages = await db.getMessages(data.session.id);
		}
	}

	return data;
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
