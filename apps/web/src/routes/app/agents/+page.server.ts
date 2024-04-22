import { supabase } from '$lib/supabase';
import { fail, error } from '@sveltejs/kit';
import { zod } from 'sveltekit-superforms/adapters';

import { agentSchema } from '$lib/schema';
import { setError, superValidate } from 'sveltekit-superforms/server';
import { pickRandomAvatar } from '$lib/utils';
import api from '$lib/api';

export const load = async ({ locals }) => {
	const userSession = await locals.getSession();
	const agents = await api
		.GET('/agents/', {
			params: {
				query: {
					profile_id: userSession.user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving agents for profile ${userSession.user.id}: ${e.detail}`);
				throw error(500, `Failed to load agents for profile ${userSession.user.id}`);
			}
			if (!d) {
				console.error(`No data returned from agents`);
				return [];
			}
			if (d.length === 0) {
				console.warn(`No agents found for profile ${userSession.user.id}`);
				return d;
			}
			return d;
		});

	const form = {
		agent: await superValidate(zod(agentSchema))
	};

	return {
		agents,
		form
	};
};

export const actions = {
	create: async ({ request, locals }) => {
		console.log('create agent');
		const userSession = await locals.getSession();

		const form = await superValidate(request, zod(agentSchema));

		if (!form.valid) {
			return fail(400, { form, message: 'unable to create a new agent' });
		}

		const randomAvatar = pickRandomAvatar();

		const agent = await api
			.POST('/agents/', {
				body: {
					profile_id: userSession.user.id,
					avatar: randomAvatar.avatarUrl,
					title: form.data.title,
					description: form.data.description,
					published: form.data.published,
					role: form.data.role,
					tools: form.data.tools,
					system_message: form.data.system_message,
					model: form.data.model,
					crew_ids: [],
					version: '1'
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error creating crew: ${e.detail}`);
					return fail(500, {
						message:
							'Agent create failed. Please try again. If the problem persists, contact support.'
					});
				}
				if (!d) {
					console.error(`No data returned from crew creation`);
					return fail(500, {
						message:
							'Agent create failed. Please try again. If the problem persists, contact support.'
					});
				}
				return d;
			});

		return { form };
	},
	update: async ({ request, locals }) => {
		console.log('update agent');
		const userSession = await locals.getSession();

		const form = await superValidate(request, zod(agentSchema));

		if (!form.valid) {
			return fail(400, { form, message: 'unable to create a new agent' });
		}

		const agent = await api
			.PATCH('/agents/{id}', {
				params: {
					path: {
						id: form.data.id
					}
				},
				body: {
					profile_id: userSession.user.id,
					title: form.data.title,
					description: form.data.description,
					published: form.data.published,
					role: form.data.role,
					tools: form.data.tools,
					system_message: form.data.system_message,
					model: form.data.model
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error creating crew: ${e.detail}`);
					throw fail(500, {
						message:
							'Agent update failed. Please try again. If the problem persists, contact support.'
					});
				}
				if (!d) {
					console.error(`No data returned from crew creation`);
					throw fail(500, {
						message:
							'Agent update failed. Please try again. If the problem persists, contact support.'
					});
				}
				return d;
			});

		return { form };
	}
};
