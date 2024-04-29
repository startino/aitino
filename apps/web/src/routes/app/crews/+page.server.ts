import { fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { createCrewSchema, editCrewSchema } from '$lib/schema';

import api from '$lib/api';

export const load = async ({ locals: { supabase, stripe, authGetUser, safeGetSession } }) => {
	const user = await authGetUser();

	const form = {
		create: await superValidate(zod(createCrewSchema)),
		edit: await superValidate(zod(editCrewSchema))
	};

	const crews = await api
		.GET('/crews/', {
			params: {
				query: {
					profile_id: user.id
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
	create: async ({ request, locals: { supabase, stripe, authGetUser, safeGetSession } }) => {
		const user = await authGetUser();
		const form = await superValidate(request, zod(createCrewSchema));
		if (!form.valid) {
			return fail(400, { form });
		}
		const { data } = form;

		const crew = await api
			.POST('/crews/', {
				body: {
					profile_id: user.id,
					...data,
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
