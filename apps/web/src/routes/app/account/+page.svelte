<script lang="ts">
	import { Plus, XCircle } from 'lucide-svelte';
	import { onMount } from 'svelte';

	import { AppShell } from '$lib/components/layout/shell';
	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { browser } from '$app/environment';
	import { getPremadeInputsMap } from '$lib/utils';
	import { slide } from 'svelte/transition';

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

	let myApi = [
		{
			name: 'googleApi',
			value: 'qwertyuokjhgfdssdfghjkertyuiqwertyuokjhgfdssdfghjkertyuiqwertyuokjhgfdssdfghjkertyui'
		},
		{
			name: 'openai',
			value: 'qwertyuokjhgfdssdfghjkertyuiqwertyuokjhgfdssdfghjkertyuiqwertyuokjhgfdssdfghjkertyui'
		}
	];

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

	let newApiName = '';
	let newApiValue = '';

	function addApi() {
		if (newApiName && newApiValue) {
			myApi = [...myApi, { name: newApiName, value: newApiValue }];
			newApiName = '';
			newApiValue = '';
		}
	}
	function toggleVisibility(index) {
		myApi[index].isVisible = !myApi[index].isVisible;
		myApi = myApi; // Trigger reactivity
	}
	function removeApi(index: number) {
		myApi = myApi.filter((_, i) => i !== index);
	}
</script>

<AppShell>
	<Tabs.Root value="profile">
		<Tabs.List class="grid w-full grid-cols-3">
			<Tabs.Trigger value="profile">Profile</Tabs.Trigger>
			<Tabs.Trigger value="billing">Billing setting</Tabs.Trigger>
			<Tabs.Trigger value="api">API</Tabs.Trigger>
		</Tabs.List>
		<Tabs.Content value="profile">
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
						<div class="mb-4 grid grid-cols-[2fr_3fr_auto] gap-4">
							<Input bind:value={input.name} />
							<Input bind:value={input.value} />
							<button on:click={() => removeInput(i)} aria-label="remove input"><XCircle /></button>
						</div>
					{/each}

					<Button
						variant="outline"
						aria-label="add input"
						class="border-border rounded-full border"
						on:click={addInput}
					>
						<Plus />
					</Button>
				</Card.Content>
			</Card.Root>
		</Tabs.Content>
		<Tabs.Content value="api">
			<Card.Root>
				<Card.Header></Card.Header>
				<Card.Content>
					<div class="mb-4 flex items-center justify-between">
						<h2 class="text-lg font-semibold">API Keys</h2>
					</div>

					<form class="mb-6 space-y-4" on:submit|preventDefault={addApi}>
						<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
							<Input placeholder="API Name" bind:value={newApiName} />
							<Input placeholder="API Value" bind:value={newApiValue} />
						</div>
						<div class="flex justify-end">
							<Button type="submit">
								<Plus class="mr-2" /> Add API
							</Button>
						</div>
					</form>
					{#if myApi.length === 0}
						<p class="text-primary-600">No API keys added yet.</p>{/if}

					<div class="space-y-4">
						{#each myApi as api, index}
							<div
								class=" bg-background flex items-center rounded-lg p-4 hover:scale-[99%] hover:shadow-xl"
								transition:slide={{ duration: 200 }}
							>
								<div class="flex-1">
									<h3 class="text-lg font-semibold">{api.name}</h3>
									<!-- svelte-ignore a11y-click-events-have-key-events -->
									<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
									<p class="cursor-pointer" on:click={() => toggleVisibility(index)}>
										{api.isVisible ? api.value : 'click to see'}
									</p>
								</div>
								<Button variant="destructive" on:click={() => removeApi(index)} class="ml-auto bg-transparent hover:bg-transparent">
									<XCircle class="text-destructive h-5 w-5" />
								</Button>
							</div>
						{/each}
					</div>
				</Card.Content>
			</Card.Root>
		</Tabs.Content>
	</Tabs.Root>
</AppShell>

