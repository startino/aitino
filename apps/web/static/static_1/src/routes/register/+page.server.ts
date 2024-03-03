import { fail, redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";
import { superValidate } from "sveltekit-superforms/server";
import { formSchema } from "$lib/schma";
import { type Provider } from "@supabase/supabase-js";

export const load = async () => {
	return {
		registerForm: await superValidate(formSchema)
	};
};

export const actions: Actions = {
	register: async ({ request, locals, url }) => {
		const body = Object.fromEntries(await request.formData());
		const session = await locals.getSession();
		console.log(session, 'session');

		const provider = url.searchParams.get("provider") as Provider;

		if (provider) {
			const { data, error: err } = await locals.supabase.auth.signInWithOAuth({
				provider: provider
			});

			console.log(data, "data from");

			if (err) {
				console.log(err);
				return fail(400, {
					message: "Something went wrong"
				});
			}

			const user = data.user;

			if (user) {
				const { error: profileError } = await locals.supabase
					.from("profiles")
					.upsert({ id: user.id, display_name: body.display_name as string });
				// .insert([{ display_name: body.display_name as string }]);

				if (profileError) {
					console.error("Failed to create user profile:", profileError);
					return fail(500, { error: "Failed to create user profile" });
				}
			}

			throw redirect(307, data.url);
		}

		const form = await superValidate(body, formSchema);

		if (!provider) {
			if (!form.valid) {
				return fail(400, {
					form,
					success: false,
					errors: form.errors
				});
			}
		}

		const { data, error: err } = await locals.supabase.auth.signUp({
			email: body.email as string,
			password: body.password as string,
			options: {
				data: {
					display_name: body.display_name as string
				}
			}
		});

		console.log(data, "from register +page.ts", err, "from register +page.ts");

		if (err) {
			return fail(400, {
				error: err.message
			});
		}

		console.log(body, "body from register +page.server.ts");
		const user = data.user;

		if (user) {
			const { error: profileError } = await locals.supabase
				.from("profiles")
				.upsert({ id: user.id, display_name: body.display_name as string });
			// .insert([{ display_name: body.display_name as string }]);

			if (profileError) {
				console.error("Failed to create user profile:", profileError);
				return fail(500, { error: "Failed to create user profile" });
			}
		}

		throw redirect(301, "/");
	}
};
