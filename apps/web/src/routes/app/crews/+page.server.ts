import { fail } from '@sveltejs/kit';
import { message, setError } from 'sveltekit-superforms';
import { superValidate } from 'sveltekit-superforms/server';
import { zod } from 'sveltekit-superforms/adapters';
import { editCrewSchema } from '$lib/schema';

import { CrewsService } from '$lib/client';

export const load = async ({ locals: { getSession } }) => {
	const session = await getSession();
	const form = await superValidate(zod(editCrewSchema));

	const crews = await CrewsService.getCrewsOfUserCrewsGet(session?.user.id as string).catch((e) => {
		console.log({ error: e });
	});

	return {
		crews,
		form
	};
};

export const actions = {
	editCrew: async ({ request }) => {
		const form = await superValidate(request, zod(editCrewSchema));

		if (!form.valid) {
			return fail(400, { form });
		}
		await CrewsService.updateCrewCrewsCrewIdPatch(form.data.id, form.data).catch((e) => {
			setError(form, e.message, { status: 500 });
		});

		return message(form, 'Changes saved successfully!');
	}
};
