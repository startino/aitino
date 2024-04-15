import { fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

import { apiKeySchema } from '$lib/schema';

// TODO: Implement api client instead of these legacy ones

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
	create: async ({ request, locals }) => {
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

		return message(form, 'API Key added!');
	},

	delete: async ({ url }) => {
		const id = url.searchParams.get('id');

		if (!id) {
			return fail(400, { message: 'No id provided' });
		}

		await ProfilesService.deleteApiKeyProfilesApiKeysApiKeyIdDelete(id).catch(() => {
			fail(500);
		});

		return { message: 'API Key deleted successfully' };
	}
};
