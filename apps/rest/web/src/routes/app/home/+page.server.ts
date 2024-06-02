import { supabase } from '$lib/supabase';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { superValidate } from 'sveltekit-superforms/server';
import type { Database, Tables, Enums } from '$lib/types/supabase';
import type { Lead } from '$lib/types/';

export const load = async ({ locals }) => {
	const session = await locals.getSession();

	const { data, error } = await supabase.from('leads').select('*');

	let leads = data as Lead[];
	return { leads };
};
export const actions: Actions = {};
