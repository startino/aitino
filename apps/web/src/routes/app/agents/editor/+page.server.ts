import { supabase } from '$lib/supabase';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { createNewAgents } from '$lib/schema';
import { superValidate } from 'sveltekit-superforms/server';
import { pickRandomAvatar } from '$lib/utils';

export const load = (async ({ locals }) => {
	const session = await locals.getSession();
	const currentUserAgents = await supabase
		.from('agents')
		.select('*')
		.eq('profile_id', session?.user.id);

	const { data: userApis, error: userApiError } = await supabase
		.from('users_api_keys')
		.select('*')
		.eq('profile_id', session?.user.id);

	const user_api_keys = userApis;

	const { data, error } = await supabase.from('api_key_types').select('*');
	const api_key_types = data;

	const agentTools = await supabase.from('tools').select('*');
	return {
		currentUserAgents,
		api_key_types,
		agentTools,
		user_api_keys,
		agentForm: await superValidate(createNewAgents)
	};
}) satisfies PageServerLoad;

export const actions: Actions = {
	creatAgents: async ({ request, locals }) => {
		const session = await locals.getSession();

		const form = await superValidate(request, createNewAgents);

		if (!form.valid) {
			return fail(400, { form, message: 'unable to create a new agent' });
		}
		console.log(form);
		const randomAvatar = pickRandomAvatar();

		let data, error;

		try {
			({ data, error } = await supabase
				.from('agents')
				.insert([
					{
						profile_id: session?.user.id,
						title: form.data.title,
						description: form.data.description,
						model: form.data.model === 'undefined' ? 'gpt-3.5-turbo' : form.data.model,
						role: form.data.role,
						published: form.data.published === 'on' ? true : false,
						system_message: form.data.system_message,
						tools: [
							{
								id: form.data.id,
								parameter: {}
							}
						],
						avatar: randomAvatar.avatarUrl,
						version: '1.0'
					}
				])
				.select());
		} catch (error) {
			console.error(error);
			return fail(500, {
				message: 'Something went wrong , please try again'
			});
		}

		if (error) {
			console.error('Error creating agent:', error);
			return { error, message: error.message };
		}

		return {
			message: 'Agent created successfully please reload the page to view your new agent'
		};
	},
	editAgent: async ({ request, url }) => {
		const id = url.searchParams.get('id');

		const form = await superValidate(request, createNewAgents);
		console.log(form, 'form');

		const currentAgent = await supabase
			.from('agents')
			.select('*')
			.eq('id', id?.split('$')[1])
			.single();

		const prev_tools = currentAgent.data.tools;

		console.log(prev_tools);

		if (!form.valid) {
			return fail(400, { form, message: 'Could not edit agent' });
		}

		console.log(form);

		let data, error;

		try {
			({ data, error } = await supabase
				.from('agents')
				.update({
					title: form.data.title,
					role: form.data.role,
					description: form.data.description,
					tools: [
						...currentAgent.data.tools,
						{
							id: form.data.id,
							parameter: {}
						}
					],
					system_message: form.data.system_message,
					model: form.data.model,
					published: form.data.published === 'on' ? true : false
				})
				.eq('id', id?.split('$')[1]));
		} catch (error) {
			console.error('something when wron when editing agent:', error);
			return fail(500, { message: 'Something went wrong, please try again' });
		}

		if (error) {
			console.error('Error editing agent:', error);
			return { error };
		}

		console.log('Agent edited successfully:', data);
		return {
			message: 'Agent edited successfully please reload to see the changes you made'
		};
	},
	removeTools: async ({ request, url }) => {
		const id = url.searchParams.get('id');
		const toolId = url.searchParams.get('toolId');
		const form = await request.formData();

		console.log(id, toolId, 'id, toolId');

		const currentAgent = await supabase.from('agents').select('*').eq('id', id).single();

		console.log(currentAgent, 'currentAgent');

		const deleteTool = currentAgent.data.tools.filter((tool) => tool.id !== toolId);
		const { data, error } = await supabase
			.from('agents')
			.update({
				tools: deleteTool
			})
			.eq('id', id);
	}
};
