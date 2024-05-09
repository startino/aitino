import { getContext as getSvelteContext, setContext as setSvelteContext } from 'svelte';
import type { Node } from '@xyflow/svelte';
import type { Writable } from 'svelte/store';
import type Stripe from 'stripe';
import type { schemas } from '$lib/api';
import type { User } from '@supabase/supabase-js';
import type { Infer, SuperValidated } from 'sveltekit-superforms';
import type { AgentSchema, CrewSchema } from './schema';

export function setContext<K extends keyof ContextMap>(key: K, value: ContextMap[K]) {
	return setSvelteContext(key, value);
}

export function getContext<K extends keyof ContextMap>(key: K): ContextMap[K] {
	return getSvelteContext<ContextMap[K]>(key);
}

export interface ContextMap {
	root: RootContext;
	crew: CrewContext;
	session: SessionContext;
	subscriptionStore: Writable<{
		sub: Stripe.Response<Stripe.Subscription> | null;
		tier: any | null;
		paymentMethod: Stripe.Response<Stripe.PaymentMethod> | null;
	}>;
}

// Contexts:

export interface RootContext {
	user: Writable<(User & schemas['Profile']) | null>;
	agents: Writable<schemas['Agent'][]>;
	publishedAgents: Writable<schemas['Agent'][]>;
	crews: Writable<schemas['Crew'][]>;
	sessions: Writable<schemas['Session'][]>;
	apiKeys: Writable<schemas['APIKey'][]>;
	forms: Writable<{
		agent: {
			sv: SuperValidated<Infer<AgentSchema>>;
		};
		crew: {
			sv: SuperValidated<Infer<CrewSchema>>;
		};
	}>;
}

export interface CrewContext {
	crew: Writable<schemas['Crew']>;
	nodes: Writable<Node[]>;
}

export interface SessionContext {
	session: Writable<schemas['Session']>;
	sessions: Writable<schemas['Session'][]>;
	crew: Writable<schemas['Crew']>;
	crews: Writable<schemas['Crew'][]>;
	messages: Writable<schemas['Message'][]>;
	agents: Writable<schemas['Agent'][]>;
}
