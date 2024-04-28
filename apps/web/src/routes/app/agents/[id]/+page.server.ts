import { redirect } from '@sveltejs/kit';
import api from '$lib/api';
import { fail, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { agentSchema } from '$lib/schema';

export const load = async ({ locals: { authGetSession }, params }) => {
	const { id } = params;
	const userSession = await authGetSession();

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
	const form = await superValidate(zod(agentSchema));

	return {
		agent,
		form
	};
};
