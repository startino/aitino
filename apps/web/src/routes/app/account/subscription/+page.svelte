<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import { getContext } from '$lib/utils.js';
	import * as Tabs from '$lib/components/ui/tabs';
	import PricingTiers from '$lib/components/pricing/PricingTiers.svelte';

	const subscriptionStore = getContext('subscriptionStore');
</script>

<Tabs.Content value="/app/account/subscription">
	<Card.Root class="overflow-hidden rounded-lg shadow-xl">
		<Card.Header class="p-6">
			<h2 class="text-2xl font-bold">
				{$subscriptionStore.sub ? 'Your Subscription' : 'Choose a subscription'}
			</h2>
		</Card.Header>
		<Card.Content class="p-6">
			{#if $subscriptionStore.sub}
				<div class="space-y-8">
					<div class="from-background-950 bg-background to-primary-800 rounded-lg">
						<div class="rounded-lg p-6 pt-2">
							<div class="mb-4 flex items-center justify-between">
								<div>
									<h4 class="text-lg font-semibold">{$subscriptionStore.tier?.name}</h4>
									<p>{$subscriptionStore.sub.plan.interval}ly Subscription</p>
								</div>
								<img src={$subscriptionStore.tier?.image} alt="" class="h-20 w-20 rounded-full" />
							</div>
							{#if $subscriptionStore.paymentMethod}
								<div class="mb-4">
									<h5 class="mb-1 font-semibold">Payment Method</h5>
									<Card.Root class="border-none bg-transparent">
										<Card.Content class="px-0 ">
											<p class="font-medium">
												<span>{$subscriptionStore.paymentMethod.card?.brand}</span>
												<span>...{$subscriptionStore.paymentMethod.card?.last4}</span>
											</p>
										</Card.Content>
									</Card.Root>
								</div>
							{/if}
							<div>
								<h5 class="mb-1 font-semibold">Renewal Date</h5>
								<p>
									{new Date($subscriptionStore.sub.current_period_end * 1000).toLocaleDateString(
										undefined,
										{
											year: 'numeric',
											month: 'long',
											day: '2-digit'
										}
									)}
								</p>
							</div>
						</div>
					</div>
					<div class="text-right">
						<AlertDialog.Root closeOnOutsideClick>
							<AlertDialog.Trigger asChild let:builder>
								<Button builders={[builder]} variant="destructive">Cancel Subscription</Button>
							</AlertDialog.Trigger>
							<AlertDialog.Content>
								<AlertDialog.Header>
									<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
									<AlertDialog.Description>
										This action cannot be undone. This will immediately cancel your subscription.
									</AlertDialog.Description>
								</AlertDialog.Header>
								<AlertDialog.Footer>
									<AlertDialog.Cancel>
										<Button
											variant="outline"
											class="border-none bg-transparent hover:bg-transparent">Close</Button
										>
									</AlertDialog.Cancel>
									<AlertDialog.Action>
										<a href="/app/subscription/cancel">
											<Button class="border-none bg-transparent hover:bg-transparent"
												>Cancel Subscription</Button
											>
										</a>
									</AlertDialog.Action>
								</AlertDialog.Footer>
							</AlertDialog.Content>
						</AlertDialog.Root>
					</div>
				</div>
			{:else}
				<PricingTiers />
			{/if}
		</Card.Content>
	</Card.Root>
</Tabs.Content>
