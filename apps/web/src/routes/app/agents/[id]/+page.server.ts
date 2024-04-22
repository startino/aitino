import { error, redirect } from '@sveltejs/kit';
import api, { type schemas } from '$lib/api';

export const load = async ({ locals: { getSession }, params }) => {
	const { id } = params;
	const userSession = await getSession();

	const agent = await api
		.GET('/agents/{id}', {
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

	if (!agent) {
		console.error(`Redirecting to '/app/agents': No crew found with id ${id}`);
		throw redirect(303, '/app/agents');
	}

	return {
		agent
	};
};
