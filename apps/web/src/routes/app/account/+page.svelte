<script lang="ts">
	import { Plus, PlusCircle, XCircle } from 'lucide-svelte';
	import { onMount } from 'svelte';

	import { AppShell } from '$lib/components/layout/shell';
	import * as Card from '$lib/components/ui/card';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { browser } from '$app/environment';
	import { getPremadeInputsMap } from '$lib/utils';
	import { slide } from 'svelte/transition';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';

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
	let apiNames = ['Google Maps', 'OpenWeather', 'Twitter API', 'Facebook API'];

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
	function toggleVisibility(index: number) {
		myApi[index].isVisible = !myApi[index].isVisible;
		myApi = myApi;
	}
	function removeApi(index: number) {
		myApi = myApi.filter((_, i) => i !== index);
	}

	// Function to handle selection
	function handleSelect(name: string) {
		newApiName = name;
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
						class="border-border rounded-full border"
						on:click={addInput}
					>
						<Plus />
					</Button>
				</Card.Content>
			</Card.Root>
		</Tabs.Content>
		<Tabs.Content value="billing">
			<Card.Root class="overflow-hidden rounded-lg shadow-xl">
				<Card.Header class="text-on-primary bg-gradient-to-r p-6">
					<h2 class="text-xl font-semibold">Membership</h2>
				</Card.Header>
				<Card.Content class="p-6">
					<div class="space-y-8">
						<div class="bg-background rounded-lg bg-gradient-to-r p-6 shadow-sm">
							<div class="text-2xl font-semibold ">Current Plan</div>
							<p class="font-medium">Starter</p>
							<div class="mt-4 flex gap-4 transition-all duration-200 ease-in-out">
								<Button class=" border bg-transparent text-current " href="/app/subscription"
									>Change Plan</Button
								>
								<Button
									class=" flex items-center gap-2 rounded-md border bg-transparent  text-current"
								>
									<Plus /> Add a promo code
								</Button>
							</div>
						</div>
						<div class="bg-background rounded-lg p-6 shadow-sm  ">
							<div class="text-2xl font-semibold">Current Billing Cycle</div>
							<p class="text-sm">Mar 20, 2024 - Apr 19, 2024</p>
						</div>
					</div>
				</Card.Content>
			</Card.Root>
		</Tabs.Content>

		<Tabs.Content value="api">
			<Card.Root>
				<Card.Header>API Keys</Card.Header>
				<Card.Content>
					<form class="mb-6" on:submit|preventDefault={addApi}>
						<div class="flex flex-wrap gap-4 md:items-end">
							<div class="max-w-lg flex-1">
								<DropdownMenu.Root>
									<DropdownMenu.Trigger asChild let:builder>
										<Button variant="outline" class="ml-auto" builders={[builder]}>
											Api provider <ChevronDown class="ml-2 h-4 w-4" />
										</Button>
									</DropdownMenu.Trigger>
									<DropdownMenu.Content class="z-50">
										{#each apiNames as name}
											<DropdownMenu.CheckboxItem
												checked={newApiName === name}
												on:click={() => handleSelect(name)}
											>
												{name}
											</DropdownMenu.CheckboxItem>
										{/each}
									</DropdownMenu.Content>
								</DropdownMenu.Root>
							</div>
							<div class="flex-grow">
								<Input
									placeholder="API Value"
									bind:value={newApiValue}
									class="w-full focus-visible:ring-1 focus-visible:ring-offset-0"
								/>
							</div>
							<Button type="submit" class="shrink-0">
								<Plus class="mr-2" /> Add API
							</Button>
						</div>
					</form>

					{#if myApi.length === 0}
						<p class="text-primary-600">No API keys added yet.</p>
					{/if}

					<div class="space-y-4">
						{#each myApi as api, index}
							<div
								class="bg-background flex items-center rounded-lg p-4 transition-all duration-300 hover:scale-[99%] hover:shadow-xl"
								transition:slide={{ duration: 200 }}
							>
								<div class="flex flex-col">
									<!-- svelte-ignore a11y-click-events-have-key-events -->
									<!-- svelte-ignore a11y-no-static-element-interactions -->
									<div class="flex">
										<h3 class="mr-1 text-lg font-semibold">{api.name}</h3>
										<span
											class="text-primary cursor-pointer"
											title={api.value}
											on:click={() => toggleVisibility(index)}>?</span
										>
									</div>
									<!-- svelte-ignore a11y-click-events-have-key-events -->
									<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->

									<div class="flex gap-6">
										<p
											class="cursor-pointer"
											on:click={() => toggleVisibility(index)}
											title={api.value}
										>
											{api.isVisible ? api.value : ' '}
										</p>
									</div>
								</div>
								<Button
									variant="destructive"
									on:click={() => removeApi(index)}
									class="ml-auto bg-transparent hover:scale-105 hover:bg-transparent"
								>
									<XCircle class="text-destructive hover:scale-105" size="18" />
								</Button>
							</div>
						{/each}
					</div>
				</Card.Content>
			</Card.Root>
		</Tabs.Content>
	</Tabs.Root>
</AppShell>
