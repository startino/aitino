import { supabase } from '$lib/supabase';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { agentFormSchema } from '$lib/schema';
import { superValidate } from 'sveltekit-superforms/server';

export const load = (async ({ locals }) => {
	const session = await locals.getSession();
	const getCurrentUserAgents = await supabase
		.from('agents')
		.select('*')
		.eq('profile_id', session?.user.id);
	return {
		getCurrentUserAgents,
		agentForm: await superValidate(agentFormSchema)
	};
}) satisfies PageServerLoad;

export const actions: Actions = {
	creatAgents: async ({ request, locals }) => {
		const session = await locals.getSession();

		const profile_id = session?.user.id;

		const form = await superValidate(request, agentFormSchema);

		if (!form.valid) {
			return fail(400, { form, message: 'Could not create agent' });
		}

		const title = form.data.title;
		const description = form.data.description.split(',').map((item: string) => item.trim());

		const model = form.data.model;
		let published = form.data.published;

		const role = form.data.role;
		const tools = '';
		const avatar =
			'https://ommkphtudcxplovqfhmu.supabase.co/storage/v1/object/public/agent-avatars/1.png';
		const version = '1.0';
		const system_message = '';

		try {
			const { data, error } = await supabase
				.from('agents')
				.insert([
					{
						profile_id,
						title,
						description,
						model,
						role,
						published,
						tools: [tools],
						avatar,
						version,
						system_message
					}
				])
				.select();

			if (error) {
				console.error('Error creating agent:', error);
				return { error };
			}

			return fail(200, {
				message: 'Agent created successfully',
				data
			});
		} catch (error) {
			console.error(error);
			return fail(500, {
				message: 'Could not create agent'
			});
		}
	},
	editAgent: async ({ request, url }) => {
		const id = url.searchParams.get('id');

		const form = await superValidate(request, agentFormSchema);

		console.log(form, 'from from agent');
		if (!form.valid) {
			return fail(400, { form, message: 'Could not edit agent' });
		}

		try {
			const { data, error } = await supabase
				.from('agents')
				.update({
					title: form.data.title,
					role: form.data.role,
					description: [form.data.description],
					model: form.data.model,
					published: form.data.published === 'true' ? true : false
				})
				.eq('id', id?.split('$')[1]);

			if (error) {
				console.error('Error editing agent:', error);
				return { error };
			}

			console.log('Agent edited successfully:', data);
			if (data === null) {
				return {};
			}
			return fail(200, {
				message: 'Agent edited successfully'
			});
		} catch (error) {
			console.error(error);
			return fail(500, {
				message: 'Could not edit agent'
			});
		}
	}
};
