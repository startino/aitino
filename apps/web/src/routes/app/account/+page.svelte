<script lang="ts">
	import { Plus, XCircle } from 'lucide-svelte';
	import { onMount } from 'svelte';

	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { browser } from '$app/environment';
	import { getPremadeInputsMap } from '$lib/utils';

	let inputs: { name: string; value: string }[] = [];

	onMount(() => {
		const premadeInputsMap = getPremadeInputsMap();

		if (premadeInputsMap) {
			inputs = Object.entries(premadeInputsMap).map(([name, value]) => ({ name, value })) as {
				name: string;
				value: string;
			}[];
		}
	});

	function addInput() {
		inputs.push({ name: '', value: '' });
		inputs = inputs;
	}

	function removeInput(index: number) {
		inputs.splice(index, 1);
		inputs = inputs;
	}

	$: {
		if (browser && inputs.length > 0) {
			const inputMap = inputs.reduce((prev, curr) => {
				if (!curr.name) return prev;
				return {
					...prev,
					[curr.name.trim()]: curr.value
				};
			}, {});

			localStorage.setItem('premade-inputs', JSON.stringify(inputMap));
		}
	}
</script>

<Tabs.Content value="/app/account">
	<Card.Root>
		<Card.Header>
			<Card.Title>Profile</Card.Title>
		</Card.Header>
		<Card.Content>
			<h2
				class="mb-8 scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0"
			>
				Premade Inputs
			</h2>

			<div class="mb-4 grid grid-cols-[2fr_3fr] gap-4">
				<span class="grow-[2]">Name</span>
				<span class="grow-[3]">Value</span>
			</div>

			{#each inputs as input, i}
				<div class="mb-4 flex w-full gap-4">
					<div class="flex w-full flex-wrap items-center gap-4">
						<div class="max-w-lg flex-1">
							<Input
								placeholder=""
								bind:value={input.value}
								class="w-full focus-visible:ring-1 focus-visible:ring-offset-0"
							/>
						</div>
						<div class="flex-grow">
							<Input
								placeholder=""
								bind:value={input.value}
								class="w-full focus-visible:ring-1 focus-visible:ring-offset-0"
							/>
						</div>
						<Button
							variant="ghost"
							class="text-destructive hover:bg-transparent"
							on:click={() => removeInput(i)}
							aria-label="remove input"><XCircle /></Button
						>
					</div>
				</div>
			{/each}

			<Button
				variant="outline"
				aria-label="add input"
				class="rounded-full border border-border"
				on:click={addInput}
			>
				<Plus />
			</Button>
		</Card.Content>
	</Card.Root>
</Tabs.Content>
