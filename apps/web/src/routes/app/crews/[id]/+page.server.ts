import { redirect } from '@sveltejs/kit';
import api, { type schemas } from '$lib/api';
import { type Node } from '@xyflow/svelte';

export const load = async ({ locals: { authGetUser }, params }) => {
	const { id } = params;
	const user = await authGetUser();

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

    // TODO: do some fancy preview + clone stuff if the crew is published so the users can share crews
    if (crew.profile_id !== user.id) {
        console.error(`Redirecting to '/app/crews': Profile ${user.id} does not have access to crew ${id}`);
        throw redirect(303, '/app/crews');
    }

	const nodes: Node[] = [];

	return {
		crew: crew,
		nodes: nodes,
		startNodes: crew.agents
	};
};
