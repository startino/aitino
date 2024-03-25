import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import type { Provider } from '@supabase/supabase-js';

export const load = (async () => {
	return {};
}) satisfies PageServerLoad;

export const actions: Actions = {
	login: async ({ request, locals, cookies, url }) => {
		const provider = url.searchParams.get('provider') as Provider;

		if (provider) {
			const { data, error: err } = await locals.supabase.auth.signInWithOAuth({
				provider: provider
			});

			if (err) {
				console.log(err);
				return fail(400, {
					message: 'Something went wrong'
				});
			}

			throw redirect(307, data.url);
		}
		const body = Object.fromEntries(await request.formData());

		if (!body.email || !body.password) {
			return fail(400, {
				error: 'Please provide your credentials to enjoy the services of Aitino'
			});
		}
		const { data, error } = await locals.supabase.auth.signInWithPassword({
			email: body.email as string,
			password: body.password as string
		});

		if (error) {
			return fail(500, {
				error: error.message
			});
		}

		throw redirect(307, '/app');
	}
};
