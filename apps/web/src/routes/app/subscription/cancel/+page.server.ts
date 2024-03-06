import { redirect } from '@sveltejs/kit';

export const load = async ({ locals: { stripe }, parent }) => {
	const { stripeSub } = await parent();

	if (!stripeSub) {
		throw redirect(303, '/app');
	}
	try {
		await stripe.subscriptions.cancel(stripeSub.id);
	} catch (err) {
		throw redirect(303, '/app');
	}

	return {
		title: 'Cancellation completed',
		message: 'Your subscription has been canceled'
	};
};
