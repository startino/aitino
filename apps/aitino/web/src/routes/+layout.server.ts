export const load = async ({ url, locals: { getUser, supabase } }) => {
	const code = url.searchParams.get('code');
	const user = await getUser();

	if (code && !user) {
		await supabase.auth.exchangeCodeForSession(code);
	}

	return {
		user: await getUser()
	};
};
