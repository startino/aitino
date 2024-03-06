<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { PaymentForm } from '$lib/components/payment-form';
	import { browser } from '$app/environment';

	export let data;

	$: ({ clientSecret, paymentMethod, newSubscriptionId, newTier, price, interval } = data);
</script>

<Card.Root class="mx-auto w-full">
	<Card.Header>
		<div class="flex items-center gap-4">
			<img src={newTier.image} class="w-28" alt="" />
			<div>
				<Card.Title>{newTier.name}</Card.Title>
				<Card.Description class="font-bold">{price}/{interval}</Card.Description>
			</div>
		</div>
	</Card.Header>

	{#if browser}
		<Card.Content>
			<PaymentForm
				{paymentMethod}
				bind:clientSecret
				returnUrl={`${window.location.origin}/app/subscription/complete?subscription_id=${newSubscriptionId}&tier_id=${newTier.id}`}
			/>
		</Card.Content>
	{/if}
</Card.Root>
