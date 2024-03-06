import { error, redirect } from '@sveltejs/kit';
import type Stripe from 'stripe';

export const load = async ({ locals: { supabase, stripe, getSession }, params, parent }) => {
	const session = await getSession();

	const { data: profile } = await supabase
		.from('profiles')
		.select()
		.eq('id', session?.user.id)
		.single();

	const { stripeSub } = await parent();

	let hasAcess = true;
	if (stripeSub) {
		try {
			if (stripeSub.status === 'active') {
				console.log('subscription active');

				hasAcess = false;
			}
		} catch (error) {
			console.log({ error });
		}
	}

	if (!hasAcess) throw redirect(302, '/app/subscription');

	let newSubscription: Stripe.Response<Stripe.Subscription>;
	const { data: newTier, error: tiersError } = await supabase
		.from('tiers')
		.select()
		.eq('slug', params.tierSlug)
		.single();

	if (!newTier || tiersError) {
		throw error(404, 'Page not found');
	}
	const price = await stripe.prices.retrieve(newTier.stripe_price_id);

	const dollars = ((price.unit_amount as number) / 100).toLocaleString('en-US', {
		style: 'currency',
		currency: 'USD'
	});

	try {
		newSubscription = await stripe.subscriptions.create({
			customer: profile.stripe_customer_id,
			items: [
				{
					price: newTier.stripe_price_id
				}
			],
			payment_behavior: 'default_incomplete',
			payment_settings: { save_default_payment_method: 'on_subscription' },
			expand: ['latest_invoice.payment_intent']
		});
	} catch (err) {
		console.log({ err });

		throw error(500, 'something went wrong');
	}

	return {
		newTier,
		clientSecret: newSubscription.latest_invoice?.payment_intent.client_secret,
		newSubscriptionId: newSubscription.id,
		price: dollars,
		interval: price.recurring?.interval
	};
};
