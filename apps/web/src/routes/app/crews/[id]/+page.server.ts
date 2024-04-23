import { error, redirect } from '@sveltejs/kit';
import api, { type schemas } from '$lib/api';
import { type Node } from '@xyflow/svelte';

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

	const nodes: Node[] = [];

	return {
		profileId: userSession.user.id,
		crew: crew,
		agents: userAgents,
		publishedAgents: publishedAgents,
		nodes: nodes,
		startNodes: crew.agents
	};
};
