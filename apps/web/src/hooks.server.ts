import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';
import { STRIPE_SECRET_KEY } from '$env/static/private';
import { createServerClient } from '@supabase/ssr';
import { error, redirect, type Handle } from '@sveltejs/kit';
import Stripe from 'stripe';
import { toast } from 'svelte-sonner';
import api from '$lib/api';

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

	event.locals.getUser = async () => {
		const {
			data: { user },
			error
		} = await event.locals.supabase.auth.getUser();

		if (!user || error) {
			return null;
		}

		const profile = await api
			.GET('/profiles/{id}', {
				params: {
					path: {
						id: user.id
					}
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error retrieving profile: ${e.detail}`);
					return null;
				}
				if (!d) {
					console.error(`No data returned from profile`);
					return null;
				}
				return d;
			});
		if (!profile) {
			return null;
		}

		return { ...user, ...profile };
	};

	event.locals.authGetUser = async () => {
		const userProfile = await event.locals.getUser();
		if (!userProfile) {
			toast('No user. Please log in.');
			redirect(303, '/login');
		}

		return userProfile;
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

		const userProfile = await event.locals.getUser();
		if (!userProfile) {
			return null;
		}

		return { ...session, ...userProfile };
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
