import { fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { emailAuthSchema } from '$lib/schema';
import { type Provider } from '@supabase/supabase-js';

export async function load({ locals: { safeGetSession } }) {
	const auth = await safeGetSession();
	if (auth) {
		redirect(303, '/app');
	}

	const form = await superValidate(zod(emailAuthSchema));

	return {
		form
	};
}

export const actions = {
	authEmail: async ({ request, locals: { supabase }, url }) => {
		const form = await superValidate(request, zod(emailAuthSchema));
		if (!form.valid) {
			return fail(400, { form });
		}
		const { data } = form;

		const { error: e } = await supabase.auth.signInWithOtp({
			email: data.email,
			options: {
				emailRedirectTo: getURL() + 'app'
			}
		});

		if (e) {
			return fail(500, {
				error: e.message
			});
		}

		throw redirect(303, '/auth/verify-email');
	},
	authProvider: async ({ locals: { supabase }, url }) => {
		const validProviders = ['google', 'github'];

		if (!url.searchParams.has('provider')) {
			return fail(400, {
				message: 'No provider given.'
			});
		}
		if (!validProviders.includes(url.searchParams.get('provider') as string)) {
			return fail(400, {
				message: 'Invalid provider'
			});
		}

		const { data, error: err } = await supabase.auth.signInWithOAuth({
			provider: url.searchParams.get('provider') as Provider,
			options: {
				redirectTo: getURL() + 'app'
			}
		});

		if (err) {
			console.error('Failed to sign in with OAuth:', err);
			return fail(500, {
				message: 'Failed to sign in with OAuth'
			});
		}

		throw redirect(307, data.url);
	}
};

const getURL = () => {
	let url =
		process?.env?.NEXT_PUBLIC_SITE_URL ?? // Set this to your site URL in production env.
		process?.env?.NEXT_PUBLIC_VERCEL_URL ?? // Automatically set by Vercel.
		`http://localhost:${process.env.PORT || 5173}/`; // Use dynamic port or default to 5173
	// Make sure to include `https://` when not localhost.
	url = url.includes('http') ? url : `https://${url}`;
	// Make sure to include a trailing `/`.
	url = url.charAt(url.length - 1) === '/' ? url : `${url}/`;
	return url;
};
