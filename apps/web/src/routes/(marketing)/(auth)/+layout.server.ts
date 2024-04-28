import { redirect } from '@sveltejs/kit';

export async function load({ locals: { safeGetSession } }) {
	const auth = await safeGetSession();
	if (auth) {
		redirect(303, '/app');
	}
}
