import { error, fail } from '@sveltejs/kit';
import { message, setError } from 'sveltekit-superforms';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { editCrewSchema } from '$lib/schema';

import api from '$lib/api';

export const load = async ({ locals: { getSession } }) => {
	const userSession = await getSession();

	const superValidated = await superValidate(zod(editCrewSchema));

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
		form: superValidated
	};
};

export const actions = {
	edit: async ({ request }) => {
		const superValidated = await superValidate(request, zod(editCrewSchema));

		if (!superValidated.valid) {
			return fail(400, { superValidated });
		}

		await api
			.PATCH(`/crews/{id}`, {
				params: {
					path: {
						id: superValidated.data.id
					}
				},
				body: {
					...superValidated.data
				}
			})
			.catch((e) => {
				setError(superValidated, e.message, { status: 500 });
			});

		return message(superValidated, 'Changes saved successfully!');
	}
};
