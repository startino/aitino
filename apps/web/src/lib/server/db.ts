import { supabase } from "$lib/supabase";
import type { TablesInsert } from "$lib/types/supabase";
import { error } from "@sveltejs/kit";
import type { Crew, Message, Session } from "$lib/types/models";

export async function getMessages(session_id: string) {

	const { data, error: err } = await supabase
		.from("messages")
		.select("*")
		.eq("session_id", session_id);
	if (err) {
		throw error(500, "Failed attempt at retrieving messages. Please reload the page.");
	}

	if (data.length === 0) {
		return [];
	}

	return data as Message[];
}

export async function renameSession(sessionId: string, newName: string) {
	const { data, error: err } = await supabase.from("sessions").update({ name: newName }).eq("id", sessionId);
	if (err) {
		throw error(500, "Failed attempt at renaming session.");
	}
}

export async function deleteSession(sessionId: string) {
	const { data, error: err } = await supabase.from("sessions").delete().eq("id", sessionId);
	if (err) {
		throw error(500, "Failed attempt at deleting session.");
	}
}

export async function postCrew(data: TablesInsert<"crews">) {
	if (!data.id) throw error(400, "Invalid Crew ID");
	if (!data.profile_id) throw error(400, "There is no profile connected to this crew. Try logging in again.");
	if (!data.title) throw error(400, "Crew is missing a title");
	if (!data.description) throw error(400, "Crew is missing a description");
	if (!data.receiver_id) throw error(400, "There's no receiver connected to this crew. Connect the prompt");
	if (!data.nodes) throw error(400, "Invalid Crew Nodes");
	if (!data.edges) throw error(400, "Invalid Crew Edges");

	return supabase.from("crews").upsert(data);
}

export async function getCrews(profileId: string) {
	const { data, error: err } = await supabase
		.from("crews")
		.select("*")
		.eq("profile_id", profileId);

	if (err) {
		return [];
	}
	if (data.length === 0) {
		return [];
	}

	const crews: Crew[] = data as Crew[];

	return crews;
}

export async function getSessions(profileId: string, crewId: string | null = null) {
	// Filter by profile_id and crewId if it exists
	const { data, error: err } = crewId ? await supabase
		.from("sessions")
		.select("*")
		.eq("profile_id", profileId)
		.eq("crew_id", crewId) : await supabase.from("sessions")
		.select("*")
		.eq("profile_id", profileId);

	if (err) {
		return [];
	}
	if (data.length === 0) {
		return [];
	}

	const sessions: Session[] = data as Session[];

	return sessions;
}

// Get the most recent session
export async function getRecentSession(profileId: string) {

	// Filter by profile_id and crewId if it exists
	const { data, error: err } = await supabase
		.from("sessions")
		.select("*")
		.eq("profile_id", profileId).order("created_at", { ascending: false }).limit(1);

	if (err) {
		return null;
	}
	if (data.length === 0) {
		return null;
	}

	const session: Session = data[0] as Session;

	return session;
}

export async function getSession(sessionId: string) {
	const { data, error: err } = await supabase
		.from("sessions")
		.select("*")
		.eq("id", sessionId).single();

	if (err) {
		return null;
	}
	if (data.length === 0) {
		return null;
	}

	const session: Session = data as Session;

	return session;
}

// Get the most recently modified Crew
export async function getRecentCrew(profileId: string) {
	// Filter by profile_id and crewId if it exists
	const { data, error: err } = await supabase
		.from("crews")
		.select("*")
		.eq("profile_id", profileId).order("updated_at", { ascending: false }).limit(1);

	if (err) {
		return null;
	}
	if (data.length === 0) {
		return null;
	}

	const crew: Crew = data[0] as Crew;

	return crew;
}