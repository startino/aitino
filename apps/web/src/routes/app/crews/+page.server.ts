import * as db from '$lib/server/db';
import { supabase } from '$lib/supabase';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const data = await db.getAllCrews();
	return {
		data
	};
};

export const actions: Actions = {
	editCrew: async ({ request, url }) => {
		const id = url.searchParams.get('id');
		const form = await request.formData();

		const title = form.get('title');
		const description = form.get('description');

		if (!id) {
			return;
		}

		console.log(form, 'form', id, 'id');

		const { data, error } = await supabase
			.from('crews')
			.update({ title, description, published: form.get('published') === 'on' ? true : false })
			.eq('id', id);

		console.log(data, 'data', error, 'error');

		if (error) {
			return fail(400, {
				success: false,
				message: error.message
			});
		}

		return {
			success: true,
			message: 'Updated Successfully'
		};
	}
};
