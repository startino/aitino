<script lang="ts">
	import { Gem } from 'lucide-svelte';
	import { onMount } from 'svelte';

	export let promotions: {
		label: string;
		index: number;
		for: string;
		discount: string;
	}[];
	export let activeTabValue = 0;

	let positionClass: string = 'left: 0px';
	let rowHeight: number = 0;

	// Offset from gap. Needs to be same as gap-x of flex-row. Unit is px.
	let rowGap: number = 4;

	// Widths of individual toggle elements (includes padding of element)
	let button_widths: number[] = [0, 0, 0, 0, 0];

	function handleClick(tabValue: number) {
		console.log(tabValue);
		let left = 0;
		button_widths.forEach((value, index) => {
			if (index < tabValue) {
				left += value + rowGap;
			}
		});

		let newString = 'left: ' + left.toString() + 'px';
		positionClass = 'left: ' + left.toString() + 'px';
		activeTabValue = tabValue;

		cycle = tabValue == 0 ? 'monthly' : 'yearly';
	}
	export let cycle: string = 'monthly';

	onMount(() => {
		handleClick(1);
	});

	function delay(ms: number) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}
</script>

<div class="{$$props.class} flex rounded-lg border border-secondary/20 bg-surface">
	<div class="relative mx-1 my-2 flex flex-row items-center gap-1 text-center">
		<div
			class="absolute rounded-lg border-2 border-primary transition-all delay-75 duration-500 ease-in-out"
			style="width: {button_widths[activeTabValue]}px; {positionClass}; height: {rowHeight}px"
		/>

		{#each promotions as { label, discount, index }, i}
			<!--{activeTabValue == promotion.index
					? 'active border-2 rounded-xl  border-primary'
					: -->
			<button
				class="rounded-lg px-4 py-4 sm:px-5 md:px-8 {activeTabValue == i
					? ''
					: 'outline outline-0 outline-white hover:outline-1'}"
				bind:clientWidth={button_widths[i]}
				bind:clientHeight={rowHeight}
				on:click={() => handleClick(index)}
			>
				<div class="flex flex-row place-items-center gap-2">
					<h1 class="title-medium uppercase tracking-wide">{label}</h1>

					{#if discount}
						<div
							class="flex flex-row place-items-center gap-1 fill-tertiary stroke-tertiary pl-1 text-tertiary"
						>
							<Gem size="18" class="text-accent" />

							<h2 class="text-xs uppercase text-accent">
								{discount}
							</h2>
						</div>
					{/if}
				</div>
			</button>
		{/each}
	</div>
</div>

<style>
</style>
