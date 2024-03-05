import * as db from '$lib/server/db';
import type { CrewLoad } from '$lib/types/loads';
import type { PageServerLoad, Actions } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies, locals: { getSession } }) => {
	const session = await getSession();
	const profileId = session?.user?.id;

	const userAgents =  db.getAgents(profileId); 
	const publishedAgents = db.getPublishedAgents();

	const userCrews = db.getCrews(profileId);
	const publishedCrews = db.getPublishedCrews();


	const data: CrewLoad = {
		profileId: profileId,
		crew: {
			id: '',
			profile_id: profileId,
			receiver_id: '',
			title: '',
			description: '',
			nodes: [],
			edges: [],
			created_at: '',
			published: false
		},
		myCrews: await userCrews,
		pulishedCrews: await publishedCrews,
		myAgents: await userAgents,
		publishedAgents: await publishedAgents
	};



	const crews = await db.getCrews(profileId);
	if (userCrews.length !== 0) {
		data.crew = userCrews[0]; // TODO: select most recent crew by default and add support for managing crew
	}

	return data;
};

export const actions: Actions = {
	save: async ({ cookies, request }) => {
		const data = await request.json();

		const { error: err } = await db.postCrew({
			id: data.id,
			profile_id: data.profile_id,
			title: data.title,
			description: data.description,
			receiver_id: data.receiver_id,
			nodes: data.nodes,
			edges: data.edges
		});

		if (err) {
			console.log(err);
			throw error(500, 'Failed attempt at saving Crew. Please try again.');
		}
	}
};
