import * as db from '$lib/server/db';
import type { CrewLoad } from '$lib/types/loads';
import type { PageServerLoad, Actions } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies, locals: { getSession } }) => {
	const session = await getSession();
	const profileId = session?.user?.id;
	const agent = await db.getAgents();

	const myAgents = agent.filter((a) => session.user.id === a.profile_id);
	const publishedAgents = agent.filter((a) => a.published === true);
	const allCrews = await db.getAllCrews();
	const myCrews = allCrews.filter((a) => 'edb9a148-a8fc-48bd-beb9-4bf5de602b78' === a.profile_id);
	const publishedCrews = allCrews.filter((a) => a.published === true);


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
		myCrews: myCrews,
		pulishedCrews: publishedCrews,
		myAgents: myAgents,
		publishedAgents: publishedAgents
	};



	const crews = await db.getCrews(profileId);
	if (crews.length !== 0) {
		data.crew = crews[0]; // TODO: select most recent crew by default and add support for managing crew
	}

	return data;
};

export const actions: Actions = {
	save: async ({ cookies, request }) => {
		const data = await request.json();

		if (!data.id) throw error(400, 'Invalid Crew ID');
		if (!data.profile_id) throw error(400, 'Invalid Profile ID');
		if (!data.title) throw error(400, 'Invalid Crew Title');
		if (!data.description) throw error(400, 'Invalid Crew Description');
		if (!data.receiver_id) throw error(400, 'Invalid Receiver ID');
		if (!data.nodes) throw error(400, 'Invalid Crew Nodes');
		if (!data.edges) throw error(400, 'Invalid Crew Edges');

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
