import { error, redirect } from '@sveltejs/kit';
import api, { type schemas } from '$lib/api';
import type { Edge, Node } from '@xyflow/svelte';

const processEdges = (crewEdges: schemas['Crew']['edges']): Edge[] => {
	let edges: Edge[] = [];

	for (let edge of crewEdges) {
		edges.push({
			id: edge.id,
			source: edge.source,
			target: edge.target,
			sourceHandle: edge.sourceHandle,
			targetHandle: edge.targetHandle,
			selected: false
		});
	}
	return edges;
};

const getNodesByCrewId = async (crew_id: string): Promise<Node[]> => {
	const agents = await api
		.GET('/agents/', {
			params: {
				query: {
					crew_id: crew_id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving agents: ${e}`);
				return null;
			}
			if (!d) {
				console.error(`No data returned from agents`);
				return null;
			}
			return d;
		});
	if (!agents) {
		return [];
	}

	let nodes: Node[] = [];

	for (let agent of agents) {
		nodes.push({
			id: agent.id,
			type: 'agent',
			position: { x: 0, y: 0 },
			selectable: false,
			data: { ...agent }
		});
	}

	return nodes;
};

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
				return null;
			}
			if (!d) {
				console.error(`No data returned from crews`);
				return null;
			}
			return d;
		});

	if (!crew) {
		console.error(`Redirecting to '/crews': No crew found with id ${id}`);
		redirect(303, '/crews');
	}

	const userAgents = await api
		.GET('/agents/', {
			params: {
				query: {
					profile_id: profileId
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving agents: ${e}`);
				return null;
			}
			if (!d) {
				console.error(`No data returned from agents`);
				return null;
			}
			return d;
		});

	const publishedAgents = await api
		.GET('/agents/', {
			params: {
				query: {
					published: true
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving agents: ${e}`);
				return null;
			}
			if (!d) {
				console.error(`No data returned from agents`);
				return null;
			}
			return d;
		});

	// null check
	if (!userAgents) {
		throw error(500, 'Failed to load user agents');
	}
	if (!publishedAgents) {
		throw error(500, 'Failed to load published agents');
	}

	return {
		profileId: profileId,
		crew: crew,
		myAgents: userAgents,
		publishedAgents: publishedAgents,
		nodes: await getNodesByCrewId(crew.id),
		edges: processEdges(crew.edges)
	};
};

export const actions = {
	save: async ({ request }) => {
		const data = await request.json();
		const prompt = data.nodes.find((n: any) => n.type === 'prompt');
		const agents = data.nodes.filter((n: any) => n.type === 'agent');

		await api
			.PATCH('/crews/{crew_id}', {
				params: {
					path: {
						crew_id: data.id
					}
				},
				body: {
					...data,
					prompt: prompt ? { id: prompt.id, ...prompt.data } : null,
					nodes: agents.map((n: any) => n.id)
				}
			})
			.catch((e) => {
				error(500, `Failed saving the Crew: ${e.toString()}`);
			});
	}
};
