<script lang="ts">
	import { formatCurrency } from '$lib/utils';
	import { features, type NorpTier } from '$lib/pricing-data';
	import { CheckCircle2, Info } from 'lucide-svelte';
	import { Button } from '../ui/button';

	export let tier: NorpTier;
	export let cycle: string = 'yearly';
</script>

<div
	class="relative flex flex-col place-items-start gap-2 text-left"
	id={tier.name.toLowerCase().replace(' ', '')}
>
	<img
		src={tier.thumbnail}
		alt=""
		class="z-0 h-fit w-1/2 translate-x-1/2 translate-y-1/4 object-cover object-center drop-shadow-pricing-art"
	/>
	<div class="z-10">
		<h2 class="text-5xl font-semibold leading-none">
			{tier.name}
		</h2>
		<h3 class="pb-6 pl-1 pt-1 text-lg text-foreground/75">
			{tier.subtitle}
		</h3>
	</div>
	<div class="flex flex-row items-end gap-2">
		<div class="flex flex-row place-items-center">
			<h1 class="text-5xl font-semibold leading-none tracking-tight text-primary">
				{cycle == 'yearly' ? formatCurrency(tier.cost * 0.833) : formatCurrency(tier.cost)}
			</h1>
		</div>
	</div>
	<h3 class="text-md text-foreground/75">per month, billed {cycle}</h3>

	<div class="px grid w-full grid-cols-2 gap-y-1 pt-2">
		<!-- Features Rows-->
		{#each Object.entries(features) as [featureName, featureAbout]}
			<div class="flex flex-row place-items-center gap-3 border-t border-foreground/50">
				<h2 class="text-md my-auto py-1 text-left">
					{featureName}
				</h2>
			</div>
			<div class="flex w-full items-center justify-items-end border-t border-foreground/50 py-1">
				{#if tier.features[featureName] == true}
					<CheckCircle2 height="24" width="24" class="ml-auto text-secondary" />
				{:else}
					<h2 class="text-md my-auto ml-auto flex place-items-end justify-self-end">
						{tier.features[featureName]}
					</h2>
				{/if}
			</div>
		{/each}
	</div>
	<Button class="mt-2 w-full" on:click={() => {}}>
		<h1 class="title-medium">GET STARTED</h1>
	</Button>
</div>
