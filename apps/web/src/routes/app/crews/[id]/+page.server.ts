import { error, redirect } from '@sveltejs/kit';
import api, { type schemas } from '$lib/api';

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

	try {
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

		const crewAgents = await api
			.GET('/agents/', {
				params: {
					query: {
						crew_id: id
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
		if (!crewAgents) {
			throw error(500, 'Failed to load crew agents');
		}

		return {
			profileId: profileId,
			crew: crew,
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
