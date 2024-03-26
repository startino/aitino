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
	import type { PageData } from './$types';
	import { enhance } from '$app/forms';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import { getContext } from '$lib/utils.js';
	import PricingTiers from '$lib/components/pricing/PricingTiers.svelte';

	const subscriptionStore = getContext('subscriptionStore');

	export let data: PageData;
	let newApiName = '';
	let newApiValue = '';

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

	$: apiTypes = data.data;

	$: myApi = data.currentUserApis;

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

	function removeApi(index: number) {
		myApi = myApi?.filter((_, i) => i !== index);
	}

	$: apiId = null;
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
						class="rounded-full border border-border"
						on:click={addInput}
					>
						<Plus />
					</Button>
				</Card.Content>
			</Card.Root>
		</Tabs.Content>
		<Tabs.Content value="billing">
			<Card.Root class="overflow-hidden rounded-lg shadow-xl">
				<Card.Header class="p-6">
					<h2 class="text-2xl font-bold">
						{$subscriptionStore.sub ? 'Your Subscription' : 'Choose a subscription'}
					</h2>
				</Card.Header>
				<Card.Content class="p-6">
					{#if $subscriptionStore.sub}
						<div class="space-y-8">
							<div class="from-background-950 rounded-lg bg-background to-primary-800">
								<div class="rounded-lg p-6 pt-2">
									<div class="mb-4 flex items-center justify-between">
										<div>
											<h4 class="text-lg font-semibold">{$subscriptionStore.tier?.name}</h4>
											<p>{$subscriptionStore.sub.plan.interval}ly Subscription</p>
										</div>
										<img
											src={$subscriptionStore.tier?.image}
											alt=""
											class="h-20 w-20 rounded-full"
										/>
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
											{new Date(
												$subscriptionStore.sub.current_period_end * 1000
											).toLocaleDateString(undefined, {
												year: 'numeric',
												month: 'long',
												day: '2-digit'
											})}
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
												This action cannot be undone. This will immediately cancel your
												subscription.
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
		<Tabs.Content value="api">
			<Card.Root>
				<Card.Header class="text-xl font-semibold">Your API Keys</Card.Header>
				<Card.Content>
					<form
						class="mb-6"
						action="?/addAPI&id={apiId !== undefined ? apiId : ''}"
						method="POST"
						use:enhance
					>
						<div class="flex flex-wrap gap-4 md:items-end">
							<div class="max-w-lg flex-1">
								<DropdownMenu.Root>
									<DropdownMenu.Trigger asChild let:builder>
										<Button variant="outline" class="ml-auto" builders={[builder]}>
											Api provider <ChevronDown class="ml-2 h-4 w-4" />
										</Button>
									</DropdownMenu.Trigger>
									<DropdownMenu.Content class="z-50">
										{#each apiTypes as apiType}
											<DropdownMenu.CheckboxItem
												checked={newApiName === apiType.name}
												on:click={() => {
													apiId = apiType.id;
												}}
											>
												{apiType.name}
											</DropdownMenu.CheckboxItem>
										{/each}
									</DropdownMenu.Content>
								</DropdownMenu.Root>
							</div>
							<div class="flex-grow">
								<Input
									placeholder="API Value"
									bind:value={newApiValue}
									name="apiValue"
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
							<form
								action="?/removeAPI&id={api.id}"
								method="POST"
								use:enhance
								class="flex items-center rounded-lg bg-background p-4 transition-all duration-300 hover:scale-[99%] hover:shadow-xl"
								transition:slide={{ duration: 200 }}
							>
								<div class="flex flex-col">
									<div class="flex">
										<h3 class="mr-1 text-lg font-semibold">{api.name}</h3>
									</div>
								</div>
								<Button
									variant="destructive"
									type="submit"
									on:click={() => {
										removeApi(index);
									}}
									class="ml-auto bg-transparent hover:scale-105 hover:bg-transparent"
								>
									<XCircle class="text-destructive hover:scale-105" size="18" />
								</Button>
							</form>
						{/each}
					</div>
				</Card.Content>
			</Card.Root>
		</Tabs.Content>
	</Tabs.Root>
</AppShell>
