// Contains types for +page.server.ts files data properties

import * as models from '$lib/types/models';

export type SessionLoad = {
	profileId: string;
	session: models.Session;
	sessions: models.Session[];
	messages: models.Message[];
	crew: models.Crew;
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
