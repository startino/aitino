export const load = async ({ locals: { supabase, stripe, getSession } }) => {
	const session = await getSession();

	const { data: billing } = await supabase
		.from('billing_information')
		.select()
		.eq('profile_id', session?.user.id)
		.single();

	const { data: subscription } = await supabase
		.from('subscriptions')
		.select()
		.eq('profile_id', session?.user.id)
		.single();

	const { data: profile } = await supabase
		.from('profiles')
		.select('tiers ( * )')
		.eq('id', session?.user.id)
		.single();

	const currentTier = profile?.tiers;

	try {
		const { card, id } = await stripe.paymentMethods.retrieve(billing.stripe_payment_method);
		const stripeSubscription = await stripe.subscriptions.retrieve(
			subscription.stripe_subscription_id
		);
		return { paymentMethod: { card, id }, stripeSubscription, currentTier };
	} catch (error) {
		console.log(error);

		return { paymentMethod: null, stripeSubscription: null, currentTier };
	}
};
