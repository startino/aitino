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

	const agentTools = await supabase.from('tools').select('*');
	return {
		currentUserAgents,
		agentTools,
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
						system_message: form.data.prompt,
						tools: [''],
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

		if (!form.valid) {
			return fail(400, { form, message: 'Could not edit agent' });
		}

		let data, error;

		try {
			({ data, error } = await supabase
				.from('agents')
				.update({
					title: form.data.title,
					role: form.data.role,
					description: form.data.description,
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
	addTools: async ({ request, url }) => {
		const id = url.searchParams.get('id');
		const toolId = url.searchParams.get('toolId');

		const currentAgent = await supabase.from('agents').select('*').eq('id', id).single();

		let currentTools = currentAgent.data.tools;

		const { data, error } = await supabase
			.from('agents')
			.update({
				tools:
					currentTools !== null
						? [...currentTools, { id: toolId, parameter: {} }]
						: [{ id: toolId, parameter: {} }]
			})
			.eq('id', id);
	},
	removeTools: async ({ request, url }) => {
		const id = url.searchParams.get('id');
		const toolId = url.searchParams.get('toolId');
		const form = await request.formData();

		const currentAgent = await supabase.from('agents').select('*').eq('id', id).single();

		const deleteTool = currentAgent.data.tools.filter((tool) => tool.id !== toolId);
		const { data, error } = await supabase
			.from('agents')
			.update({
				tools: deleteTool
			})
			.eq('id', id);
	}
};
