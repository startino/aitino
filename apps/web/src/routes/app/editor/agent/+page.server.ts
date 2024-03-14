import { supabase } from '$lib/supabase';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load = (async ({ locals }) => {
	const session = await locals.getSession();
	const getCurrentUserAgents = await supabase
		.from('agents')
		.select('*')
		.eq('profile_id', session?.user.id);
	return {
		getCurrentUserAgents
	};
}) satisfies PageServerLoad;

export const actions: Actions = {
	creatAgents: async ({ request, locals }) => {
		const session = await locals.getSession();

		const profile_id = session?.user.id;

		const formData = Object.fromEntries(await request.formData());

		console.log(formData, 'form data', formData.published);
		const title = formData.title;
		const description = formData.description.split(',').map((item: string) => item.trim());
		const model = formData.model;
		const published = formData.published
		const role = formData.role;
		const tools = '';
		const avatar =
			'https://ommkphtudcxplovqfhmu.supabase.co/storage/v1/object/public/agent-avatars/1.png';
		const version = '1.0';
		const system_message = '';

		if (!title || title === '') {
			return fail(400, {
				message: 'Title is required'
			});
		}

		if (!description || description[0] === '') {
			return fail(400, {
				message: 'Description is required'
			});
		}

		if (!role || role === '') {
			return fail(400, {
				message: 'Role is required'
			});
		}

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
						tools,
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

			console.log('Agent created successfully:', data);

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

		console.log(url.searchParams, 'url search params');
		const formData = Object.fromEntries(await request.formData());
		console.log(formData, 'form data', id?.split('$')[1], 'id');

		try {
			const { data, error } = await supabase
				.from('agents')
				.update({
					title: formData.title,
					role: formData.role,
					description: [formData.description],
					model: formData.model
				})
				.eq('id', id?.split('$')[1]);

			if (error) {
				console.error('Error editing agent:', error);
				return { error };
			}

			console.log('Agent edited successfully:', data);

			return fail(200, {
				message: 'Agent edited successfully',
				data
			});
		} catch (error) {
			console.error(error);
			return fail(500, {
				message: 'Could not edit agent'
			});
		}
	}
};
