import type Stripe from 'stripe';
import { error } from '@sveltejs/kit';

export const load = async ({ locals: { supabase, stripe, authGetUser } }) => {
	const user = await authGetUser();
	console.log('user', user);

	// TODO: convert to using api

	const data: {
		stripeSub: Stripe.Response<Stripe.Subscription> | null;
		paymentMethod: Stripe.Response<Stripe.PaymentMethod> | null;
		userTier: any;
		tiersList: any[];
	} = { stripeSub: null, paymentMethod: null, userTier: null, tiersList: [] };

	const { data: subscription } = await supabase
		.from('subscriptions')
		.select()
		.eq('profile_id', user.id)
		.single();

	const { data: tiersList } = await supabase.from('tiers').select();

	data.tiersList = tiersList ?? [];

	data.userTier = user?.tiers as any; // TODO: don't use any

	const { data: billing } = await supabase
		.from('billing_information')
		.select()
		.eq('profile_id', user.id)
		.single();

	try {
		data.paymentMethod = await stripe.paymentMethods.retrieve(billing.stripe_payment_method);
	} catch (error) {
		data.paymentMethod = null;
	}

	try {
		const stripeSubscription = await stripe.subscriptions.retrieve(
			subscription.stripe_subscription_id
		);

		data.stripeSub = stripeSubscription.status === 'canceled' ? null : stripeSubscription;
	} catch (error) {
		data.stripeSub = null;
	}

	return {
		user,
		...data
	};
};
