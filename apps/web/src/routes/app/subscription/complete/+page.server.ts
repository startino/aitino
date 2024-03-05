import { redirect } from "@sveltejs/kit";

export const load = async ({ url, locals: { stripe, session, supabase } }) => {
	const id = url.searchParams.get("payment_intent");
	const subscriptionId = url.searchParams.get("subscription_id");
	const tierId = url.searchParams.get("tier_id");

	if (!id || !subscriptionId || !tierId) redirect(303, "/app/subscription");

	const paymentIntent = await stripe.paymentIntents.retrieve(id);

	let message: string = "";

	switch (paymentIntent.status) {
		case "succeeded":
			message = "Your subscription is successfully completed!";

			await supabase
				.from("subscriptions")
				.upsert({ profile_id: session.user.id, stripe_subscription_id: subscriptionId });

			await supabase.from("profiles").update({ tier_id: tierId }).eq("id", session.user.id);

			// TODO: provision account here

			break;

		case "processing":
			message = "Payment processing. We'll update you when payment is received.";
			break;

		case "requires_payment_method":
			// Redirect user back to payment page to re-attempt payment
			throw redirect(303, "/app/subscription");

		default:
			message = "Something went wrong.";
			break;
	}

	return { message };
};
