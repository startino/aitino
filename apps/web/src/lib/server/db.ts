import { supabase } from "$lib/supabase";
import type { TablesInsert } from "$lib/types/supabase";
import { error } from "@sveltejs/kit";
import type { Crew, Session } from "$lib/types/models";

export async function getMessages(session_id: string | null) {
	if (!session_id) {
		return [];
	}
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

	return data;
}

export async function postCrew(data: TablesInsert<"crews">) {
	if (!data.id) throw error(400, "Invalid Crew ID");
	if (!data.profile_id) throw error(400, "Invalid Profile ID");
	if (!data.title) throw error(400, "Invalid Crew Title");
	if (!data.description) throw error(400, "Invalid Crew Description");
	if (!data.receiver_id) throw error(400, "Invalid Receiver ID");
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

export async function getSessions(profileId: string, crewId: string) {
	const { data, error: err } = await supabase
		.from("sessions")
		.select("*")
		.eq("profile_id", profileId)
		.eq("crew_id", crewId);

	if (err) {
		return [];
	}
	if (data.length === 0) {
		return [];
	}

	const sessions: Session[] = data as Session[];

	return sessions;
}
