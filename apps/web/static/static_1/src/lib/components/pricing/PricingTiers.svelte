<script lang="ts">
	import PromotionToggle from "./PromotionToggle.svelte";
	import { promotions, norpTiers, features } from "$lib/pricing-data";
	import MobileTierListing from "./MobileTierListing.svelte";
	import { Button } from "$lib/components/ui/button";
	import * as Tooltip from "$lib/components/ui/tooltip";

	import { formatCurrency } from "$lib/utils";
	import { CheckCircle2, Info } from "lucide-svelte";

	let cycle: string = "yearly";
</script>

<section class="z-20">
	<div class="{$$props.class} flex flex-col items-center justify-items-center gap-8 text-center">
		<PromotionToggle class="my-4" bind:cycle {promotions} />

		<!-- Mobile view -->
		<div class="flex w-full flex-col place-items-start -space-y-16 lg:hidden">
			{#each norpTiers as tier}
				<MobileTierListing {tier} {cycle} />
			{/each}
		</div>
		<!-- Non-mobile view -->
		<div class="mt-20 hidden grid-cols-4 place-items-center lg:grid">
			<!--Top Row-->
			<div class="grid-item border-none" />
			{#each norpTiers as { name, subtitle, cost, thumbnail }}
				<div
					class=" grid-item flex max-w-md flex-col place-items-start gap-2 border-none text-left"
					id={name.toLowerCase().replace(" ", "")}
				>
					<img
						src={thumbnail}
						alt=""
						class="object-fit h-1/2 w-1/2 object-center pb-1 drop-shadow-pricing-art"
					/>
					<div class="">
						<h2 class="text-3xl font-semibold uppercase">
							{name}
						</h2>
						<h3 class="text-md pb-6 text-foreground/75">
							{subtitle}
						</h3>
					</div>
					<div class="mt-auto pb-10">
						<div class="flex flex-row items-end gap-2">
							<div class="flex flex-row place-items-center">
								<h1 class="text-4xl font-semibold leading-none tracking-tight text-primary">
									{cycle == "yearly" ? formatCurrency((cost * 10) / 12) : formatCurrency(cost)}
								</h1>
							</div>
						</div>
						<h3 class="body-medium mt-3 text-foreground/75">
							per month, billed {cycle}
						</h3>
					</div>
				</div>
			{/each}

			<!-- Features Rows-->
			{#each Object.entries(features) as [featureName, featureAbout]}
				<div class="grid-item flex flex-row items-center gap-3">
					<h2 class="text-md my-auto py-2 text-left font-semibold text-foreground">
						{featureName}
					</h2>

					<Tooltip.Root>
						<Tooltip.Trigger asChild let:builder>
							<Button builders={[builder]} variant="icon"
								><Info class="text-foreground/75 hover:text-inherit" size="18" /></Button
							>
						</Tooltip.Trigger>
						<Tooltip.Content>
							<p>{featureAbout}</p>
						</Tooltip.Content>
					</Tooltip.Root>
				</div>
				{#each norpTiers as tier}
					<div class="grid-item flex items-center self-center">
						{#if tier.features[featureName] == true}
							<CheckCircle2 size="18" class="-ml-0.5 text-secondary" />
						{:else}
							<h2 class=" title-medium text-left">
								{tier.features[featureName]}
							</h2>
						{/if}
					</div>
				{/each}
			{/each}

			<div class="grid-item border-none" />
			{#each norpTiers as tier, index}
				<div class="-ml-2 mt-10 w-full self-start md:pr-4 lg:pr-10">
					<Button class="w-full" on:click={() => {}} disabled={index == 0 ? false : true}>
						<h1 class="lg:title-large text-lg font-semibold uppercase text-primary-foreground">
							Get Started
						</h1>
					</Button>
				</div>
			{/each}
		</div>
	</div>
</section>

<style>
	.grid-item {
		@apply h-full w-full border-t border-outline/50 px-3 py-1;
	}
</style>
