import { error, redirect } from '@sveltejs/kit';
import api, { type schemas } from '$lib/api';
import type { Node } from '@xyflow/svelte';
import { getWritablePrompt } from '$lib/utils.js';

const getNodesByCrewId = async (crew: schemas['Crew']): Promise<Node[]> => {
	const agents = await api
		.GET('/agents/', {
			params: {
				query: {
					crew_id: crew.id
				}
			}
		})
		.then(async ({ data: d, error: e }) => {
			if (e) {
				console.error(`Failed to load agents for crew ${crew}. ${e.detail}. Using HEAVY fallback`);
				let a: schemas['Agent'][] = [];
				for (let agentId of crew.nodes) {
					console.log(`Using fallback for agent ${agentId}`);
					const ag = await api
						.GET('/agents/{id}', {
							params: {
								path: {
									id: agentId
								}
							}
						})
						.then(({ data: d2, error: e2 }) => {
							if (e2) {
								console.error(`Failed to load agent ${agentId}. ${e2.detail}`);
								return;
							}
							if (!d2) {
								console.error(`No data returned from agent ${agentId}`);
								return;
							}
							return d2;
						});
					if (!ag) {
						console.error(`Skipping null agent ${agentId}`);
						continue;
					}
					if (a.find((a: schemas['Agent']) => a.id === ag.id)) {
						console.error(`Skipping duplicate agent ${ag.id}`);
						continue;
					}
					a = [...a, ag];
				}
				console.log(JSON.stringify(a));
				return a;
			}
			if (!d) {
				console.error(`No data returned from agents`);
				return [];
			}
			return d;
		});

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
	const userSession = await getSession();

	const crew: schemas['Crew'] | null = await api
		.GET('/crews/{id}', {
			params: {
				path: {
					id: id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving crews: ${e.detail}`);
				return null;
			}
			if (!d) {
				console.error(`No data returned from crews`);
				return null;
			}
			return d;
		});

	if (!crew) {
		console.error(`Redirecting to '/app/crews': No crew found with id ${id}`);
		throw redirect(303, '/app/crews');
	}

	const userAgents = await api
		.GET('/agents/', {
			params: {
				query: {
					profile_id: userSession.user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving agents for profile ${userSession.user.id}: ${e.detail}`);
				throw error(500, `Failed to load agents for profile ${userSession.user.id}`);
			}
			if (!d) {
				console.error(`No data returned from agents`);
				return [];
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
				console.error(`Error retrieving published agents: ${e.detail}`);
				throw error(500, `Failed to load published agents`);
			}
			if (!d) {
				console.error(`No data returned from agents`);
				return [];
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

	const nodes = getWritablePrompt(await getNodesByCrewId(crew));

	return {
		profileId: userSession.user.id,
		crew: crew,
		agents: userAgents,
		publishedAgents: publishedAgents,
		nodes: nodes
	};
};
