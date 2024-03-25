import * as db from '$lib/server/db';
import type { NoSessionLoad } from '$lib/types/loads';
import * as models from '$lib/types/models';
import type { PageServerLoad, Actions } from './$types';
import { error, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ url, locals: { getSession } }) => {
	const userSession = await getSession();
	if (!userSession) throw error(401, 'You are not logged in. Please log in and try again.');

	const session = await db.getRecentSession(userSession.user.id);

	if (session && !url.searchParams.has('debug')) {
		redirect(303, `/app/session/${session.id}`);
	}

	const crews: models.Crew[] = await db.getCrews(userSession.user.id);

	const data: NoSessionLoad = {
		profileId: userSession.user.id,
		crews: crews
	};

	return data;
};
