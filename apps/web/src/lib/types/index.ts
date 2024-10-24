import type { Edge, Node } from '@xyflow/svelte';
import type { Writable } from 'svelte/store';

import type { Variant } from '$lib/components/ui/button';
import type Stripe from 'stripe';
import type { schemas } from '$lib/api';

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
	session: SessionContext;
	subscriptionStore: Writable<{
		sub: Stripe.Response<Stripe.Subscription> | null;
		tier: any | null;
		paymentMethod: Stripe.Response<Stripe.PaymentMethod> | null;
	}>;
}

export interface CrewContext {
	profileId: Writable<string>;
	crew: Writable<schemas['Crew']>;
	agents: Writable<schemas['Agent'][]>;
	publishedAgents: Writable<schemas['Agent'][]>;
	nodes: Writable<Node[]>;
}

export interface SessionContext {
	profileId: Writable<string>;
	session: Writable<schemas['Session']>;
	sessions: Writable<schemas['Session'][]>;
	crew: Writable<schemas['Crew']>;
	crews: Writable<schemas['Crew'][]>;
	messages: Writable<schemas['Message'][]>;
	agents: Writable<schemas['Agent'][]>;
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
