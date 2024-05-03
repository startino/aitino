import { error, redirect } from '@sveltejs/kit';

export async function load({ locals: { supabase } }) {
	const { error: e } = await supabase.auth.signOut();

	if (e) {
		console.error('Error logging out');
		throw error(500, 'Error logging out, please try again or manually clear your cookies.');
	}

	throw redirect(303, '/');
}
