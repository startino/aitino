import * as db from '$lib/server/db';
import type { Crew } from '$lib/types/models';
import type { CrewLoad } from '$lib/types/loads';
import type { PageServerLoad, Actions } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies, locals: { getSession, supabase } }) => {
	const session = await getSession();
	const profileId = session?.user?.id as string;

	let crew: Crew = {
		id: crypto.randomUUID(),
		profile_id: profileId,
		receiver_id: '',
		title: 'Untitled Crew',
		description: 'No description',
		nodes: [],
		edges: [],
		created_at: '',
		published: false,
		avatar: '',
		prompt: null
	};

	const userAgents = db.getAgents(profileId);
	const publishedAgents = db.getPublishedAgents();

	const userCrews = await db.getCrews(profileId);

	crew = userCrews[0] ?? crew;

	console.log({ crew });

	const { data: crewAgents, error } = await supabase.from('agents').select().in('id', crew.nodes);

	if (!error) {
		console.log({ crewAgents });
		// maps agents data to svelte flow nodes
		crew.nodes = crewAgents.map((a) => ({
			id: a.id,
			type: 'agent',
			position: { x: 0, y: 0 },
			selectable: false,
			data: { ...a }
		}));

		crew.prompt &&
			crew.nodes.push({
				id: crew.prompt.id,
				type: 'prompt',
				position: { x: 0, y: 0 },
				data: { ...crew.prompt }
			});
	}

	const publishedCrews = db.getPublishedCrews();

	const data: CrewLoad = {
		profileId: profileId,
		crew,
		myCrews: userCrews,
		pulishedCrews: await publishedCrews,
		myAgents: await userAgents,
		publishedAgents: await publishedAgents
	};

	return data;
};

export const actions: Actions = {
	save: async ({ cookies, request, locals }) => {
		const data = await request.json();
		const prompt = data.nodes.find((n: any) => n.type === 'prompt');
		const agents = data.nodes.filter((n: any) => n.type === 'agent');

		const { error: err } = await db.postCrew({
			id: data.id,
			profile_id: data.profile_id,
			title: data.title,
			description: data.description,
			receiver_id: data.receiver_id,
			prompt: prompt ? { id: prompt.id, ...prompt.data } : null,
			nodes: agents.map((n: any) => n.id),
			edges: data.edges
		});

		if (err) {
			console.log(err);
			throw error(500, 'Failed attempt at saving Crew. Please try again.');
		}
	}
};
