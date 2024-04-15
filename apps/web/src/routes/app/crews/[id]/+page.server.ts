import type { CrewWithNodesData } from '$lib/types';
import { error } from '@sveltejs/kit';
import type { Edge } from '@xyflow/svelte';
import api from '$lib/api';

export const load = async ({ locals: { getSession }, params }) => {
	const { id } = params;
	const session = await getSession();
	const profileId = session?.user?.id as string;

	const crew = await api
		.GET('/crews/{crew_id}', {
			params: {
				path: {
					crew_id: id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving crews: ${e}`);
				return [];
			}
			if (!d) {
				console.error(`No data returned from crews`);
				return [];
			}
			return d;
		});

	let crewWithAgents: CrewWithNodesData = { ...crew, nodes: [], edges: crew.edges as Edge[] };

	try {
		const userAgents = await AgentsService.getUsersAgentsAgentsByProfileGet(profileId);
		const publishedAgents = await AgentsService.getPublishedAgentsAgentsPublishedGet();
		const crewAgents = await AgentsService.getAgentsFromCrewAgentsByCrewGet(id);

		// maps agents data to svelte flow nodes
		crewWithAgents.nodes = crewAgents.map((a) => ({
			id: a.id,
			type: 'agent',
			position: { x: 0, y: 0 },
			selectable: false,
			data: { ...a }
		}));

		crewWithAgents.prompt &&
			crewWithAgents.nodes.push({
				id: crewWithAgents.prompt.id,
				type: 'prompt',
				position: { x: 0, y: 0 },
				data: { ...crew.prompt }
			});

		return {
			profileId: profileId,
			crew: crewWithAgents,
			myAgents: userAgents,
			publishedAgents: publishedAgents
		};
	} catch (e) {
		error(500, 'Somthing went wrong');
	}
};

export const actions = {
	save: async ({ request }) => {
		const data = await request.json();
		const prompt = data.nodes.find((n: any) => n.type === 'prompt');
		const agents = data.nodes.filter((n: any) => n.type === 'agent');
		await CrewsService.updateCrewCrewsCrewIdPatch(data.id, {
			...data,
			prompt: prompt ? { id: prompt.id, ...prompt.data } : null,
			nodes: agents.map((n: any) => n.id)
		}).catch(() => {
			error(500, 'Failed saving the Crew...');
		});
	}
};
