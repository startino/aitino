// Contains types for +page.server.ts files data properties

import * as models from "$lib/types/models";

export type SessionLoad = {
	profileId: string;
	crewId: string | null;
	session: models.Session | null;
	messages: models.Message[];
	reply: string;
};

export type CrewLoad = {
	profileId: string;
	crew: models.Crew;
};
