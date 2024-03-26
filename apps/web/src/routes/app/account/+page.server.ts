import { supabase } from '$lib/supabase';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
	const session = await locals.getSession();
	const { data, error } = await supabase.from('api_key_types').select('*');
	const { data: userData, error: userError } = await supabase
		.from('users_api_keys')
		.select('*')
		.eq('profile_id', session?.user.id);

	const currentUserApis = data?.filter((d) => userData?.some((u) => u.api_key_type_id === d.id));

	return {
		data,
		currentUserApis
	};
};

export const actions: Actions = {
	addAPI: async ({ request, locals, url }) => {
		const id = url.searchParams.get('id');
		const session = await locals.getSession();
		const body = await request.formData();

		const apiValue = body.get('apiValue') as string;

		if (!id || !apiValue) {
			return fail(400, {
				message: 'Missing required fields'
			});
		}
		const { data, error } = await supabase.from('users_api_keys').insert({
			profile_id: session?.user.id,
			api_key_type_id: id,
			api_key: apiValue
		});

		if (error) {
			console.log(error, 'error');
			return fail(400, {
				message: error.message
			});
		}

		return {
			data
		};
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
