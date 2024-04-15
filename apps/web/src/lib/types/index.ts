import type { Edge, Node } from '@xyflow/svelte';
import type { Writable } from 'svelte/store';

import type { Variant } from '$lib/components/ui/button';
import type Stripe from 'stripe';

import type { schemas } from '$lib/api';

export type CrewWithNodesData = Omit<schemas['Crew'], 'nodes'> & { nodes: Node[]; edges: Edge[] };

export type SvelteEvent<E extends Event = Event, T extends EventTarget = Element> = E & {
	currentTarget: EventTarget & T;
};

export type PanelAction = {
	name: string;
	loading?: boolean;
	buttonVariant?: Variant;
	onclick?: (e: Event) => void;
	isCustom?: boolean;
};

export interface ContextMap {
	crew: CrewContext;
	subscriptionStore: Writable<{
		sub: Stripe.Response<Stripe.Subscription> | null;
		tier: any | null;
		paymentMethod: Stripe.Response<Stripe.PaymentMethod> | null;
	}>;
}

export interface CrewContext {
	receiver: Writable<{ node: Node; targetCount: number } | null>;
	count: Writable<{ agents: number; prompts: number }>;
}

export type Categories =
	| 'multi-agents'
	| 'automation'
	| 'tutorial'
	| 'reviews'
	| 'top-softwares'
	| 'ai'
	| 'learning'
	| 'mathematics'
	| 'engineering'
	| 'computer-science'
	| 'economics'
	| 'business'
	| 'art'
	| 'music'
	| 'technology'
	| 'science-fiction';
