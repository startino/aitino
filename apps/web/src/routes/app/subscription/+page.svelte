<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import PricingTiers from '$lib/components/pricing/PricingTiers.svelte';

	export let data;

	let { currentTier, stripeSubscription, paymentMethod } = data;
</script>

<h1 class="pb-10 text-4xl">Your Subscription</h1>

<div class="space-y-6 py-8">
	{#if stripeSubscription && stripeSubscription.status === 'active'}
		<div class="grid gap-4 lg:grid-cols-[auto_1fr] lg:gap-10">
			<div class="grid justify-items-center">
				<h2 class="text-3xl text-accent">
					{currentTier?.name} / {stripeSubscription.plan.interval}ly
				</h2>
				<img src={currentTier?.image} alt="" class="max-w-sm" />
			</div>

			<div class="space-y-6">
				{#if paymentMethod}
					<Card.Root class="border-2 border-accent-foreground">
						<Card.Header>
							<Card.Title>Card</Card.Title>
						</Card.Header>
						<Card.Content>
							<p class="font-bold">
								<span class="text-xl uppercase">{paymentMethod.card?.brand}</span>
								<span>...{paymentMethod.card?.last4}</span>
							</p>
						</Card.Content>
					</Card.Root>
				{/if}

				<p>
					Renewal Date: {new Date(stripeSubscription.current_period_end * 1000).toLocaleDateString(
						undefined,
						{
							year: 'numeric',
							month: 'long',
							day: '2-digit'
						}
					)}
				</p>

				<AlertDialog.Root closeOnOutsideClick>
					<AlertDialog.Trigger asChild let:builder>
						<Button builders={[builder]} variant="destructive" class="justify-self-start"
							>Cancel Subscription</Button
						>
					</AlertDialog.Trigger>
					<AlertDialog.Content>
						<AlertDialog.Header>
							<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
							<AlertDialog.Description>
								This action cannot be undone. This will immediatly cancel your subscription
							</AlertDialog.Description>
						</AlertDialog.Header>
						<AlertDialog.Footer>
							<AlertDialog.Cancel>Close</AlertDialog.Cancel>
							<AlertDialog.Action
								><a href="/app/subscription/cancel">Cancel subscription</a></AlertDialog.Action
							>
						</AlertDialog.Footer>
					</AlertDialog.Content>
				</AlertDialog.Root>
			</div>
		</div>
	{:else}
		<PricingTiers />
	{/if}
</div>
