import { redirect } from '@sveltejs/kit';
import api from '$lib/api';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { agentSchema } from '$lib/schema';

export const load = async ({ locals: { authGetUser }, params }) => {
	const { id } = params;
	const user = await authGetUser();

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

	// TODO: do some fancy preview + clone stuff if the agent is published so the users can share agents
	if (agent.profile_id !== user.id) {
		console.error(
			`Redirecting to '/app/crews': Profile ${user.id} does not have access to crew ${id}`
		);
		throw redirect(303, '/app/crews');
	}


	return {
		agent
	};
};
