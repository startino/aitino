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
						prompt: form.data.prompt,
						tools: [''],
						avatar: randomAvatar.avatarUrl,
						version: '1.0',
						system_message: ''
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
					prompt: form.data.prompt,
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
		console.log('id:', toolId);
		const form = await request.formData();

		const name = form.get('toolName');
		const description = form.get('toolDescription');
		const apiKey = form.get('apiKey');

		const currentAgent = await supabase.from('agents').select('*').eq('id', id).single();

		let currentTools = currentAgent.data.tools;
		console.log('currentAgent:', currentTools);

		const { data, error } = await supabase
			.from('agents')
			.update({
				tools:
					currentTools !== null
						? [...currentTools, { id: toolId, parameter: {} }]
						: [{ id: toolId, parameter: {} }]
			})
			.eq('id', id);

		console.log('form:', data, error);
	},
	removeTools: async ({ request, url }) => {
		const id = url.searchParams.get('id');
		const toolId = url.searchParams.get('toolId');
		console.log('toolid:', toolId);
		console.log('id:', id);
		const form = await request.formData();

		const name = form.get('toolName');

		const currentAgent = await supabase.from('agents').select('*').eq('id', id).single();
		console.log('currentAgent:', currentAgent.data.tools);

		const deleteTool = currentAgent.data.tools.filter((tool) => tool.id !== toolId);

		console.log(deleteTool, 'dele');
		console.log(currentAgent, 'cu dele');
		console.log(name, 'name');

		// // let currentTools = currentAgent.data.tools;
		// // console.log('currentAgent:', currentTools);

		const { data, error } = await supabase
			.from('agents')
			.update({
				tools: deleteTool
			})
			.eq('id', id);

		console.log('form:', data, error);
	}
};
