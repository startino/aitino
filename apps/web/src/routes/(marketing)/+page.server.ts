import { fail } from '@sveltejs/kit';
import { supabase } from '$lib/supabase';
import { zod } from 'sveltekit-superforms/adapters';
import { superValidate } from 'sveltekit-superforms/server';
import { formSchema } from '../schema';
import { waitlistSchema } from '$lib/schema';

export const load = async (event) => {
	const contactForm = await superValidate(zod(formSchema));
	const waitlistForm = await superValidate(zod(waitlistSchema));

	// Always return { form } in load and form actions.
	return { contactForm, waitlistForm };
};

export const actions = {
	register: async ({ request }) => {
		const waitlistForm = await superValidate(request, zod(waitlistSchema));

		if (!waitlistForm.valid) {
			return fail(400, {
				waitlistForm
			});
		}

		const { email } = waitlistForm.data;

		// check if user already register

		const selectAll = await supabase.from('waitlist_users').select('*').eq('email', email).single();
		// console.log(selectAll, 'all emails');

		const check_if_user_already_register = await supabase
			.from('waitlist_users')
			.select('*')
			.eq('email', email)
			.single();

		// console.log(check_if_user_already_register, 'check if user already register');
		if (check_if_user_already_register && check_if_user_already_register.data !== null) {
			return fail(400, {
				invalid: true,
				error: 'You have already joined the waitlist. See you Soon 👋'
			});
		}

		const { data, error } = await supabase
			.from('waitlist_users')
			.insert([{ email: email }])
			.select();

		if (error) {
			return fail(400, {
				invalid: true,
				error: error.message
			});
		}

		return {
			success: true,
			message: 'You have successfuly joined the waitlist. See you Soon 👋'
		};
	},
	contactUs: async ({ request }) => {
		const form = await superValidate(request, zod(formSchema));

		console.log(form, 'from backend');

		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		const { name, email, description } = form.data;

		console.log(form.data.name, form.data.email, form.data.description);

		const { data, error } = await supabase
			.from('contact_form')
			.insert([{ name: name, email: email, description: description }])
			.select();

		if (error) {
			return fail(400, {
				invalid: true
			});
		}

		return {
			success: true
		};
	}
};
