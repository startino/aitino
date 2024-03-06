<script lang="ts">
	import { PUBLIC_STRIPE_KEY } from '$env/static/public';
	import { invalidate } from '$app/navigation';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import Label from '$lib/components/ui/label/label.svelte';
	import { Elements, CardNumber, CardCvc, CardExpiry } from 'svelte-stripe';
	import { onMount } from 'svelte';
	import {
		loadStripe,
		type PaymentMethod,
		type Stripe,
		type StripeElements
	} from '@stripe/stripe-js';
	import { Button } from '$lib/components/ui/button';
	import { goto } from '$app/navigation';
	import { getContext } from '$lib/utils';

	export let clientSecret: string;
	export let returnUrl: string;
	export let paymentMethod: PaymentMethod | null = null;

	const subStore = getContext('subscriptionStore');

	let stripe: Stripe;

	let save = true;
	let processing = false;

	let elements: StripeElements;

	const cardStyle = { base: { color: '#fff' } };

	onMount(async () => {
		stripe = (await loadStripe(PUBLIC_STRIPE_KEY)) as Stripe;
	});

	async function payFromSavedCard() {
		if (processing || !paymentMethod) return;

		processing = true;

		const { paymentIntent, error } = await stripe.confirmCardPayment(clientSecret, {
			payment_method: paymentMethod.id
		});

		if (error) {
			console.error({ error });
			processing = false;
			return;
		}

		await invalidate('/app');
		if (paymentIntent) {
			goto(`${returnUrl}&payment_intent=${paymentIntent.id}`);
		}
	}

	async function submit() {
		if (processing) return;

		processing = true;

		const cardNumber = elements.getElement('cardNumber');
		if (!cardNumber) {
			console.log('No card number');
			return;
		}
		if (save) {
			const { paymentMethod } = await stripe.createPaymentMethod({
				type: 'card',
				card: cardNumber
			});

			if (!paymentMethod) {
				console.error('no payment method');
				return;
			}

			const response = await fetch('/api/save-payment-method', {
				method: 'POST',
				body: JSON.stringify({ paymentMethod: paymentMethod.id }),
				headers: {
					'Content-Type': 'application/json'
				}
			});

			const { error } = await response.json();

			if (error) {
				console.error(error);

				processing = false;
				return;
			}
			$subStore.paymentMethod = paymentMethod;
		}

		const { paymentIntent, error } = await stripe.confirmCardPayment(clientSecret, {
			payment_method: {
				card: cardNumber
			}
		});

		if (error) {
			console.error({ error });
			processing = false;
			return;
		}

		await invalidate('/app');
		if (paymentIntent) {
			goto(`${returnUrl}&payment_intent=${paymentIntent.id}`);
		}
	}
</script>

{#if stripe}
	{#if paymentMethod}
		<p class="text-lg">
			Use your saved payment method: <span class="font-bold text-accent">
				{paymentMethod.card?.brand} ...{paymentMethod.card?.last4}
			</span>
		</p>

		<Button class="mt-4" disabled={processing} on:click={payFromSavedCard}>
			{processing ? 'Processing...' : 'Pay'}
		</Button>
	{:else}
		<Elements {stripe} bind:elements>
			<form class="grid gap-3 rounded-2xl" on:submit|preventDefault={submit}>
				<CardNumber style={cardStyle} classes={{ base: 'input' }} />

				<div class="flex gap-2 [&>*]:w-1/5">
					<CardExpiry style={cardStyle} classes={{ base: 'input' }} />
					<CardCvc style={cardStyle} classes={{ base: 'input' }} />
				</div>

				<div class="mt-6 flex items-center space-x-2">
					<Checkbox id="save" bind:checked={save} />
					<Label
						for="save"
						class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
					>
						Save billing information
					</Label>
				</div>

				<Button type="submit" class="mt-4 w-full" disabled={processing}>
					{processing ? 'Processing...' : 'Pay'}
				</Button>
			</form>
		</Elements>
	{/if}
{/if}

<style lang="postcss">
	:global(.input) {
		border: solid 1px theme(colors.ring);
		padding: 1rem;
		border-radius: 5px;
		color: white !important;
		background: theme(colors.black);
	}
</style>
