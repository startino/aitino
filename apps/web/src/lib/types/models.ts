import type { Edge, Node } from '@xyflow/svelte';

export type Message = {
	id: string;
	session_id: string;
	content: string;
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
};

export type Session = {
	id: string;
	title: string;
	crew_id: string;
	profile_id: string;
	created_at: string;
};

export type Agent = {
	id: string;
	created_at: string;
	updated_at: string;
	name: string;
	description: string[];
	summary: string;
	author: string;
	model: string;
	published: boolean;
	profile_id: string;
	tools: string[];
	avatar_url: string;
	version: string
};
