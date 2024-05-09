import { fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';

import api from '$lib/api';
import { crewSchema } from '$lib/schema.js';

export const actions = {
	create: async ({ request, locals: { authGetUser } }) => {
		const user = await authGetUser();
		const form = await superValidate(request, zod(crewSchema));
		if (!form.valid) {
			return fail(400, { form });
		}
		const { data } = form;

		const crew = await api
			.POST('/crews/', {
				body: {
					profile_id: user.id,
					...data,
					receiver_id: '00000000-0000-0000-0000-000000000000',
					agents: []
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error creating crew: ${e.detail}`);
					return null;
				}
				if (!d) {
					console.error(`No data returned from crew creation`);
					return null;
				}
				return d;
			});

		if (!crew) {
			return fail(500, {
				form,
				message: 'Crew creation failed. Please try again. If the problem persists, contact support.'
			});
		}

		throw redirect(303, `/app/crews/${crew.id}`);
	}
};
