import { fail, redirect } from '@sveltejs/kit';
import { message, setError } from 'sveltekit-superforms';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { createCrewSchema, editCrewSchema } from '$lib/schema';

import api from '$lib/api';

export const load = async ({ locals: { getSession } }) => {
	const userSession = await getSession();

	const form = {
		create: await superValidate(zod(createCrewSchema)),
		edit: await superValidate(zod(editCrewSchema))
	};

	const crews = await api
		.GET('/crews/', {
			params: {
				query: {
					profile_id: userSession.user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving crews: ${e.detail}`);
				return [];
			}
			if (!d) {
				console.error(`No data returned from crews`);
				return [];
			}
			return d;
		});

	return {
		crews,
		form
	};
};

export const actions = {
	create: async ({ request, locals: { getSession } }) => {
		const userSession = await getSession();
		const form = await superValidate(request, zod(createCrewSchema));
		if (!form.valid) {
			return fail(400, { form });
		}
		const { data } = form;

		const crew = await api
			.POST('/crews/', {
				body: {
					profile_id: userSession.user.id,
					...data,

					receiver_id: '00000000-0000-0000-0000-000000000000',
					prompt: { id: '00000000-0000-0000-0000-000000000000', title: 'prompt', content: '' },
					edges: [],
					nodes: []
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error creating crew: ${e.detail}`);
					throw setError(
						form,
						'Crew creation failed. Please try again. If the problem persists, contact support.'
					);
				}
				if (!d) {
					console.error(`No data returned from crew creation`);
					throw setError(
						form,
						'Crew creation failed. Please try again. If the problem persists, contact support.'
					);
				}
				return d;
			});

		throw redirect(303, `/app/crews/${crew.id}`);
	}
};
