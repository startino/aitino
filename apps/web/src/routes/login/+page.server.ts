import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";
import type { Provider } from "@supabase/supabase-js";
import { z } from "zod";

const loginUserSchema = z.object({
	email: z.string().email({ message: "Invalid email address" }),
	password: z
		.string()
		.min(8, { message: "Password must be at least 8 characters long." })
		.max(100, { message: "Password must be 100 characters or less." })
		.regex(/[a-z]/, { message: "Password must contain at least one lowercase letter." })
		.regex(/[A-Z]/, { message: "Password must contain at least one uppercase letter." })
		.regex(/[0-9]/, { message: "Password must contain at least one number." })
});

export const load = (async () => {
	return {};
}) satisfies PageServerLoad;

export const actions: Actions = {
	login: async ({ request, locals, cookies, url }) => {
		const provider = url.searchParams.get("provider") as Provider;
	
		if (provider) {
			const { data, error: err } = await locals.supabase.auth.signInWithOAuth({
				provider: provider
			});

			if (err) {
				console.log(err);
				return fail(400, {
					message: "Something went wrong"
				});
			}

			throw redirect(307, data.url);
		}
		const body = Object.fromEntries(await request.formData());

		if (!body.email || !body.password) {
			return fail(400, {
				error: "Email or password are missing "
			});
		}
		const { data, error } = await locals.supabase.auth.signInWithPassword({
			email: body.email as string,
			password: body.password as string
		});

		if (error) {
			return fail(500, {
				error: error.message
			});
		}

		throw redirect(307, "/");
	}
};
