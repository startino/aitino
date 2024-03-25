// Contains types for .server.ts files data properties

import * as models from '$lib/types/models';
import type Stripe from 'stripe';

export type AppLoad = {
	profileId: string;
	stripeSub: Stripe.Response<Stripe.Subscription> | null;
	paymentMethod: Stripe.Response<Stripe.PaymentMethod> | null;
	userTier: any;
	tiersList: any[];
};

export type SessionLoad = {
	profileId: string;
	session: models.Session;
	sessions: models.Session[];
	crew: models.Crew;
	crews: models.Crew[];
	messages: models.Message[];
	agents: models.Agent[];
};

export type NoSessionLoad = {
	profileId: string;
	crews: models.Crew[];
};

export type CrewLoad = {
	profileId: string;
	crew: models.Crew;
	myCrews: models.Crew[];
	pulishedCrews: models.Crew[];
	myAgents: models.Agent[];
	publishedAgents: models.Agent[];
};
