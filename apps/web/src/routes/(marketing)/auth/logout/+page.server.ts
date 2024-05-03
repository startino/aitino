import { error, redirect } from '@sveltejs/kit';

export async function load({ locals: { supabase } }) {
	await supabase.auth.signOut();

	throw redirect(303, '/');
}
