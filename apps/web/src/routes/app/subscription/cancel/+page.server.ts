import { error, redirect } from "@sveltejs/kit";

export const load = async ({ locals: { stripe }, parent }) => {
	const { stripeSubscription } = await parent();

	if (!stripeSubscription) {
		throw redirect(303, "/app");
	}
	try {
		await stripe.subscriptions.cancel(stripeSubscription.id);
	} catch (err) {
		throw redirect(303, "/app");
	}

	return {
		title: "Cancellation completed",
		message: "Your subscription has been canceled"
	};
};
