import { error, fail } from '@sveltejs/kit';
import { message, setError } from 'sveltekit-superforms';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { editCrewSchema } from '$lib/schema';

import api from '$lib/api';

export const load = async ({ locals: { getSession } }) => {
	const userSession = await getSession();

	const form = await superValidate(zod(editCrewSchema));

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
	editCrew: async ({ request }) => {
		const form = await superValidate(request, zod(editCrewSchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		await api
			.PATCH(`/crews/{crew_id}`, {
				params: {
					path: {
						crew_id: form.data.id
					}
				},
				body: {
					...form.data
				}
			})
			.catch((e) => {
				setError(form, e.message, { status: 500 });
			});

		return message(form, 'Changes saved successfully!');
	}
};
