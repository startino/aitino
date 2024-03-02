import type { Node } from "@xyflow/svelte";
import type { Writable } from "svelte/store";

import type { Variant } from "$lib/components/ui/button";
import type { Tables } from "$lib/types/supabase";

export type Crew = Tables<"crews">;

export type SvelteEvent<E extends Event = Event, T extends EventTarget = Element> = E & {
	currentTarget: EventTarget & T;
};

export type PanelAction = {
	name: string;
	buttonVariant: Variant;
	onclick?: (e: Event) => void;
	isCustom?: boolean;
};

export type ContextKey = keyof ContextMap;

export interface ContextMap {
	crew: CrewContext;
}

export interface CrewContext {
	receiver: Writable<{ node: Node; targetCount: number } | null>;
	count: Writable<{ agents: number; prompts: number }>;
}

export type Categories =
	| "multi-agents"
	| "automation"
	| "tutorial"
	| "reviews"
	| "top-softwares"
	| "ai"
	| "learning"
	| "mathematics"
	| "engineering"
	| "computer-science"
	| "economics"
	| "business"
	| "art"
	| "music"
	| "technology"
	| "science-fiction";
