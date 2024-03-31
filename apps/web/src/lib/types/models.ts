import type { Edge, Node } from '@xyflow/svelte';

export type Message = {
	id: string;
	session_id: string | null;
	content: string | null;
	sender_id: string;
	recipient_id: string;
	created_at: string;
	profile_id: string;
};

export type Crew = {
	id: string;
	profile_id: string;
	receiver_id: string | null;
	title: string;
	description: string;
	nodes: Node[];
	edges: Edge[];
	created_at: string;
	published: boolean;
	avatar: string;
	prompt: { id: string; content: string } | null;
};

export type Session = {
	id: string;
	title: string;
	crew_id: string;
	profile_id: string;
	reply: string;
	status: string;
	created_at: string;
	last_opened_at: string;
};

export type Agent = {
	id: string | null;
	created_at: string;
	updated_at: string;
	title: string;
	description: string;
	role: string;
	author: string;
	model: string;
	published: boolean;
	system_message: string;
	profile_id: string;
	tools: string[];
	avatar: string;
	version: string;
};
