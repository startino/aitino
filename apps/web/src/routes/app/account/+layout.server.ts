import { ProfilesService } from '$lib/client';

export const load = async ({ locals }) => {
	const session = await locals.getSession();
	const { data: apiKeyTypes, error } = await locals.supabase.from('api_key_types').select('*');

	const userApiKeys = await ProfilesService.getApiKeysProfilesProfileIdApiKeysGet(
		session?.user.id as string
	);

	return {
		apiKeyTypes,
		userApiKeys
	};
};
