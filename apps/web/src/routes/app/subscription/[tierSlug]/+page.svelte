<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { PaymentForm } from '$lib/components/payment-form';
	import { browser } from '$app/environment';

	export let data;

	let { clientSecret, paymentMethod, subscriptionId, tier, price, interval } = data;
</script>

<Card.Root class="mx-auto w-full">
	<Card.Header>
		<div class="flex items-center gap-4">
			<img src={tier.image} class="w-28" alt="" />
			<div>
				<Card.Title>{tier.name}</Card.Title>
				<Card.Description class="font-bold">{price}/{interval}</Card.Description>
			</div>
		</div>
	</Card.Header>

	{#if browser}
		<Card.Content>
			<PaymentForm
				{paymentMethod}
				bind:clientSecret
				returnUrl={`${window.location.origin}/app/subscription/complete?subscription_id=${subscriptionId}&tier_id=${tier.id}`}
			/>
		</Card.Content>
	{/if}
</Card.Root>
