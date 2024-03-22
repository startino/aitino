// Contains types for +page.server.ts files data properties

import * as models from '$lib/types/models';

export type SessionsLoad = {
	profileId: string;
	session: models.Session | null;
	sessions: models.Session[];
	messages: models.Message[];
	crew: models.Crew | null;
	reply: string;
};

export type CrewLoad = {
	profileId: string;
	crew: models.Crew;
	myCrews: models.Crew[];
	pulishedCrews: models.Crew[];
	myAgents: models.Agent[];
	publishedAgents: models.Agent[];
};
