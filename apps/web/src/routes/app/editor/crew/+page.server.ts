import * as db from '$lib/server/db';
import type { CrewLoad } from '$lib/types/loads';
import type { PageServerLoad, Actions } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies, locals: { getSession } }) => {
	const session = await getSession();
	const profileId = session?.user?.id;

	const userAgents = db.getAgents(profileId);
	const publishedAgents = db.getPublishedAgents();

	const userCrews = await db.getCrews(profileId);
	const publishedCrews = db.getPublishedCrews();

	const data: CrewLoad = {
		profileId: profileId,
		crew: userCrews[0] ?? {
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
		myCrews: userCrews,
		pulishedCrews: await publishedCrews,
		myAgents: await userAgents,
		publishedAgents: await publishedAgents
	};

	return data;
};

export const actions: Actions = {
	save: async ({ cookies, request }) => {
		const data = await request.json();
		const prompt = data.nodes.find((n: any) => n.type === 'prompt');

		const { error: err } = await db.postCrew({
			id: data.id,
			profile_id: data.profile_id,
			title: data.title,
			description: data.description,
			receiver_id: data.receiver_id,
			prompt: prompt ? { id: prompt.id, ...prompt.data } : null,
			nodes: data.nodes.filter((n: any) => n.type === 'agent').map((n: any) => n.id),
			edges: data.edges
		});

		if (err) {
			console.log(err);
			throw error(500, 'Failed attempt at saving Crew. Please try again.');
		}
	}
};
