import {supabase} from '$lib/supabase';
import {fail} from '@sveltejs/kit';
import type {Actions, PageServerLoad} from './$types';

export const load = (async ({locals}) => {
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
	creatAgents: async ({request, locals}) => {
		const session = await locals.getSession();

		const profile_id = session?.user.id;

		const formData = Object.fromEntries(await request.formData());

		const title = formData.title;
		const description = formData.description.split(',').map((item: string) => item.trim());
		const model = formData.model;
		const role = formData.role;
		const tools = formData.tools.split(',').map((item: string) => item.trim());
		const avatar =
			'https://ommkphtudcxplovqfhmu.supabase.co/storage/v1/object/public/agent-avatars/1.png';
		const version = '1.0';
		const system_message = '';

		try {
			if (
				(title.trim().length > 0,
				description.trim().length > 0,
				model.trim().length > 0,
				role.trim().length > 0,
				tools.trim().length > 0)
			) {
				const {data, error} = await supabase
					.from('agents')
					.insert([
						{
							profile_id,
							title,
							description,
							model,
							role,
							tools,
							avatar,
							version,
							system_message
						}
					])
					.select();
			}

			if (error) {
				console.error('Error creating agent:', error);
				return {error};
			}

			console.log('Agent created successfully:', data);

			return fail(200, {
				message: 'Agent created successfully',
				data
			});
			return {data};
		} catch (error) {
			console.error(error);
			return fail(500, {
				message: 'Could not create agent'
			});
		}
	}
};
