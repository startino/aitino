import { fail } from '@sveltejs/kit';
import { zod } from 'sveltekit-superforms/adapters';
import { SAMPLE_FULL_NAMES } from '$lib/config';
import { agentSchema } from '$lib/schema';
import { superValidate } from 'sveltekit-superforms/server';
import api from '$lib/api';
import type { SupabaseClient } from '@supabase/supabase-js';

function getRandomIndex(array: Array<unknown>) {
	const randomArray = new Uint32Array(1);
	crypto.getRandomValues(randomArray);
	return randomArray[0] % array.length;
}

const pickRandomName = () => {
	const genders = ['male', 'female'];
	const genderKey = genders[getRandomIndex(genders)];

	const namesArray = SAMPLE_FULL_NAMES[genderKey];
	const name = namesArray[getRandomIndex(namesArray)];

	return { name, gender: genderKey };
};

const pickRandomAvatar = (supabase: SupabaseClient) => {
	const { name, gender } = pickRandomName();
	let avatarIndex = getRandomIndex(Array.from({ length: 23 }, (_, i) => i));

	if (gender === 'female') avatarIndex += 25;
	const avatarPath = `agent-avatars/${gender}/`;

	const { data } = supabase.storage.from(avatarPath).getPublicUrl(`${avatarIndex}.png`);
	return { name, avatarUrl: data.publicUrl };
};

export const actions = {
	create: async ({ request, locals: { supabase, authGetUser } }) => {
		console.log('create agent');
		const userSession = await authGetUser();

		const form = await superValidate(request, zod(agentSchema));

		if (!form.valid) {
			return fail(400, { form, message: 'unable to create a new agent' });
		}

		const randomAvatar = pickRandomAvatar(supabase);

		const agent = await api
			.POST('/agents/', {
				body: {
					profile_id: userSession.id,
					avatar: randomAvatar.avatarUrl,
					title: form.data.title,
					description: form.data.description,
					published: form.data.published,
					role: form.data.role,
					tools: [],
					system_message: form.data.system_message,
					model: form.data.model,
					version: '1'
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error creating crew: ${e.detail}`);
					return null;
				}
				if (!d) {
					console.error(`No data returned from crew creation`);
					return null;
				}
				return d;
			});

		if (!agent) {
			return fail(500, {
				message: 'Agent create failed. Please try again. If the problem persists, contact support.'
			});
		}
	}
};
