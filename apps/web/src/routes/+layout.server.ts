export const load = async ({ locals: { getUser } }) => {
	return {
		user: await getUser()
	};
};
