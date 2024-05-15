import { error, fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import api from '$lib/api';

import { apiKeySchema } from '$lib/schema';

export const load = async ({ locals: { supabase, stripe, authGetSession, safeGetSession }}) => {
	const userSession = await authGetSession();

	const userApiKeys = await api
		.GET('/api-keys/', {
			params: {
				query: {
					profile_id: userSession.user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving api keys: ${e.detail}`);
				return [];
			}
			if (!d) {
				console.error(`No data returned from api keys`);
				return [];
			}
			return d;
		});

	const apiKeyTypes = await api.GET('/api_providers/').then(({ data: d, error: e }) => {
		if (e) {
			console.error(`Error retrieving api key types: ${e}`);
			return [];
		}
		if (!d) {
			console.error(`No data returned from api key types`);
			return [];
		}
		return d;
	});

	const form = await superValidate(zod(apiKeySchema));
	return { form, apiKeyTypes, userApiKeys };
};

export const actions = {
	create: async ({ request, locals: { supabase, stripe, authGetSession, safeGetSession }}) => {
		const userSession = await authGetSession();

		const form = await superValidate(request, zod(apiKeySchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		await api
			.POST('/api-keys/', {
				body: {
					profile_id: userSession.user.id,
					api_key: form.data.value,
					api_provider_id: form.data.typeId
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error creating api key: ${e.detail}`);
				}
				return d;
			});

		return message(form, 'API Key added!');
	},

	delete: async ({ url }) => {
		const id = url.searchParams.get('id');

		if (!id) {
			return fail(400, { message: 'No id provided' });
		}

		await api
			.DELETE(`/api-keys/{api_key_id}`, {
				params: { path: { api_key_id: id } }
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error deleting api key: ${e.detail}`);
				}
				return d;
			});

		return { message: 'API Key deleted successfully' };
	}
};
