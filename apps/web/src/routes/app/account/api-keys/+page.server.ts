import { fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

import { supabase } from '$lib/supabase';
import { apiKeySchema } from '$lib/schema';
import { ProfilesService, ApiKeyTypesService } from '$lib/client';

export const load = async ({ locals }) => {
	const form = await superValidate(zod(apiKeySchema));
	const session = await locals.getSession();

	const userApiKeys = await ProfilesService.getApiKeysProfilesProfileIdApiKeysGet(
		session?.user.id as string
	);

	const apiKeyTypes = await ApiKeyTypesService.getAllApiKeyTypesApiKeyTypesGet();

	return { form, apiKeyTypes, userApiKeys };
};

export const actions = {
	add: async ({ request, locals }) => {
		const form = await superValidate(request, zod(apiKeySchema));

		if (!form.valid) {
			return fail(400, { form });
		}

		const session = await locals.getSession();

		const data = await ProfilesService.insertApiKeyProfilesApiKeysPost({
			profile_id: session?.user.id as string,
			api_key: form.data.value,
			api_key_type_id: form.data.typeId
		}).catch((e) => {
			return setError(form, 'Something went wrong', { status: 500 });
		});

		console.log(data);

		return message(form, 'API Key added!');
	},

	removeAPI: async ({ locals, url }) => {
		const id = url.searchParams.get('id');
		const session = await locals.getSession();

		if (!id) {
			return fail(400, {
				message: 'Missing required fields'
			});
		}
		const { data, error } = await supabase
			.from('users_api_keys')
			.delete()
			.match({ api_key_type_id: id, profile_id: session?.user.id });

		if (error) {
			console.log(error);
			return { status: 500, body: { error: 'Internal Server Error' } };
		}

		return { message: 'API Key deleted successfully' };
	}
};
