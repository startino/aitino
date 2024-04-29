import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';
import { STRIPE_SECRET_KEY } from '$env/static/private';
import { createServerClient } from '@supabase/ssr';
import { redirect, type Handle } from '@sveltejs/kit';
import Stripe from 'stripe';
import { toast } from 'svelte-sonner';
import type { User } from '@supabase/supabase-js';

export const handle: Handle = async ({ event, resolve }) => {
	event.locals.stripe = new Stripe(STRIPE_SECRET_KEY);

	event.locals.supabase = createServerClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY, {
		cookies: {
			get: (key) => event.cookies.get(key),
			/**
			 * Note: You have to add the `path` variable to the
			 * set and remove method due to sveltekit's cookie API
			 * requiring this to be set, setting the path to an empty string
			 * will replicate previous/standard behaviour (https://kit.svelte.dev/docs/types#public-types-cookies)
			 */
			set: (key, value, options) => {
				event.cookies.set(key, value, { ...options, path: '/' });
			},
			remove: (key, options) => {
				event.cookies.delete(key, { ...options, path: '/' });
			}
		}
	});

	event.locals.getUser = async (): Promise<User | null> => {
		const {
			data: { user },
			error
		} = await event.locals.supabase.auth.getUser();
		if (!user || error) {
			return null;
		}
		return user;
	};

	event.locals.authGetUser = async () => {
		const user = await event.locals.getUser();
		if (!user) {
			toast('No user. Please log in.');
			redirect(303, '/login');
		}
		return user;
	};

	/**
	 * Unlike `supabase.auth.getSession()`, which returns the session _without_
	 * validating the JWT, this function also calls `getUser()` to validate the
	 * JWT before returning the session.
	 */
	event.locals.safeGetSession = async () => {
		const {
			data: { session }
		} = await event.locals.supabase.auth.getSession();
		if (!session) {
			return null;
		}

		const user = await event.locals.getUser();
		if (!user) {
			// JWT validation has failed
			return null;
		}

		return { session, user };
	};

	event.locals.authGetSession = async () => {
		const auth = await event.locals.safeGetSession();
		if (!auth) {
			toast('No session or user. Please log in.');
			redirect(303, '/login');
		}
		return auth;
	};

	return resolve(event, {
		filterSerializedResponseHeaders(name) {
			return name === 'content-range';
		}
	});
};
