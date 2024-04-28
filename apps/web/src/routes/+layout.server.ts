import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals: { safeGetSession } }) => {
	const auth = await safeGetSession();

	return {
		session: auth?.session,
		user: auth?.user
	};
};
