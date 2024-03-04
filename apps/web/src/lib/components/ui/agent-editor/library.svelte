<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs';
	import * as Avatar from '$lib/components/ui/avatar';
	import { Input } from '$lib/components/ui/input';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import * as Card from '$lib/components/ui/card';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import User from 'lucide-svelte/icons/user';
	import { fade, fly } from 'svelte/transition';
	import * as Dialog from '$lib/components/ui/dialog';
	import type { Agent } from '$lib/types/models';
	// import Agent from '../custom-node/agent.svelte';

	export let agent: Agent[];

	console.log(agent, 'from library');

	let searchQuery = '';
	console.log(searchQuery, 'search query');
	let filterPublished = false;
	let filterModel = '';
	function updateSearchQuery(event: Event) {
		const input = event.target as HTMLInputElement;
		searchQuery = input.value;
	}

	function togglePublished() {
		filterPublished = !filterPublished;
	}

	function updateFilterModel(model: string) {
		if (filterModel === model) {
			filterModel = '';
		} else {
			filterModel = model;
		}
	}

	$: filteredAgents = agent.filter(
		(a) =>
			(searchQuery === '' ||
				a.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.description.some((desc) => desc.toLowerCase().includes(searchQuery.toLowerCase()))) &&
			(!filterPublished || a.published) &&
			(filterModel === '' || a.model === filterModel)
	);

	$: showNoResults = filteredAgents.length === 0 && searchQuery !== '';

	let showDetails = false;
	let displayedAgent: Agent;
	let showDetailInTheModal = async (id: string) => {
		displayedAgent = agent.find((a) => a.id === id);
		console.log(displayedAgent, 'new Agent');
	};
</script>

<div class="w-full max-w-6xl py-4">
	<Tabs.Root value="personal" class="h-screen max-h-[650px]">
		<Tabs.List class="sticky grid w-full grid-cols-2">
			<Tabs.Trigger value="personal">Personal</Tabs.Trigger>
			<Tabs.Trigger value="community">Community</Tabs.Trigger>
		</Tabs.List>
		<div class="w-full">
			<div class="flex items-center py-2">
				<Input
					class="max-w-4xl"
					placeholder="Search agents..."
					type="text"
					on:input={updateSearchQuery}
				/>
				<DropdownMenu.Root>
					<DropdownMenu.Trigger asChild let:builder>
						<Button variant="outline" class="ml-auto" builders={[builder]}>
							Filter <ChevronDown class="ml-2 h-4 w-4" />
						</Button>
					</DropdownMenu.Trigger>
					<DropdownMenu.Content class="z-50">
						<DropdownMenu.CheckboxItem checked={filterPublished} on:click={togglePublished}>
							Published
						</DropdownMenu.CheckboxItem>
						<DropdownMenu.CheckboxItem
							checked={filterModel === 'gpt-3'}
							on:click={() => updateFilterModel('gpt-3')}
						>
							GPT-3
						</DropdownMenu.CheckboxItem>
						<DropdownMenu.CheckboxItem
							checked={filterModel === 'gpt-4'}
							on:click={() => updateFilterModel('gpt-4')}
						>
							GPT-4
						</DropdownMenu.CheckboxItem>
					</DropdownMenu.Content>
				</DropdownMenu.Root>
			</div>
		</div>
		<Tabs.Content
			value="personal"
			class="h-5/6 space-y-6 overflow-y-scroll [&::-webkit-scrollbar]:hidden"
		>
			{#each filteredAgents as agent}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div
					class="cursor-pointer"
					transition:fade={{ delay: 500, duration: 400 }}
					on:click={() => ((showDetails = true), showDetailInTheModal(agent.id))}
				>
					<Card.Root>
						<div class="flex items-center justify-between px-6">
							<div class="flex gap-4 gap-y-4 p-4">
								<div class="flex h-20 w-20 items-center justify-center rounded-full border">
									<img src={agent.avatar_url} alt={agent.name} class="rounded-full" />
								</div>
								<div class="flex flex-col">
									<div>{agent.name}</div>
									<div>{agent.author}</div>
								</div>
							</div>
							<div class="flex h-full items-center justify-between">
								<Button variant="ghost" class="text-foreground max-w-xs  px-12 hover:bg-transparent"
									>see more</Button
								>
								<button
									class="ring-offset-background focus-visible:ring-ring bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground inline-flex h-10 max-w-xs items-center justify-center whitespace-nowrap rounded-md px-12 py-2 text-sm font-bold transition-colors hover:scale-[98%] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
									on:click|stopPropagation={(event) => console.log('not showing the details')}
									>Load</button
								>
							</div>
						</div>
						<Card.Content>
							<div class="flex justify-between">
								<p class="max-w-4xl px-6">
									{agent.summary}
								</p>
								<div class="justify-self-end">{agent.updated_at.split('T')[0]}</div>
							</div>
						</Card.Content>
					</Card.Root>
				</div>
			{/each}
			{#if showNoResults}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>

		<Tabs.Content
			value="community"
			class="h-5/6 space-y-6 overflow-y-scroll [&::-webkit-scrollbar]:hidden"
		>
			{#each filteredAgents.filter((a) => a.published) as agent}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div
					class="cursor-pointer hover:scale-[101%]"
					transition:fade={{ delay: 500, duration: 400 }}
					on:click={() => (showDetails = true,showDetailInTheModal(agent.id))}
				>
					<Card.Root>
						<div class="flex items-center justify-between px-6">
							<div class="z-50 flex gap-4 gap-y-4 p-4">
								<div class="flex h-20 w-20 items-center justify-center rounded-full border">
									<img src={agent.avatar_url} alt={agent.name} class="rounded-full" />
								</div>
								<div class="flex flex-col">
									<div>{agent.name}</div>
									<div>{agent.author}</div>
								</div>
							</div>
							<div class="flex h-full items-center justify-between">
								<Button variant="ghost" class="text-foreground max-w-xs px-12 hover:bg-transparent"
									>see more</Button
								>
								<button
									class="ring-offset-background focus-visible:ring-ring bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground inline-flex h-10 max-w-xs items-center justify-center whitespace-nowrap rounded-md px-12 py-2 text-sm font-bold transition-colors hover:scale-[98%] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
									on:click|stopPropagation={(event) => console.log('not showing the details')}
									>Load</button
								>
							</div>
						</div>
						<Card.Content>
							<div class="flex justify-between" on:click={() => (showDetails = true)}>
								<p class="max-w-4xl px-6">
									{agent.summary}
								</p>
								<div class="justify-self-end">{agent.updated_at.split('T')[0]}</div>
							</div>
						</Card.Content>
					</Card.Root>
				</div>
			{/each}
			{#if showNoResults}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>
	</Tabs.Root>
</div>

<div class="w-full max-w-6xl border">
	<Dialog.Root open={showDetails} onOpenChange={() => (showDetails = false)}>
		<Dialog.Content class="w-full max-w-6xl">
			<Dialog.Header>
				<div class="flex justify-between">
					<div class="flex h-20 w-20 items-center justify-center rounded-full border">
						<img src={displayedAgent.avatar_url} alt={displayedAgent.name} class="rounded-full" />
					</div>
					<div class="flex flex-col">
						<small class="mt-4">last update: {displayedAgent.updated_at.split('T')[0]}</small>
						<small>published at: {displayedAgent.created_at.split('T')[0]}</small>
					</div>
				</div>
				<Dialog.Description class="flex flex-col gap-y-4">
					<div>Name: {displayedAgent.name}</div>
					<div>Author: {displayedAgent.author}</div>
				</Dialog.Description>
			</Dialog.Header>
			<div class="flex w-full flex-col">
				Description:
				{#each displayedAgent.description as description}
					<ul>
						<li>{description}</li>
					</ul>
				{/each}
				<div class=" w-full text-nowrap">
					{displayedAgent.summary}
				</div>
				<!-- add loop later  -->
				<ul>
					tools:

					{#each displayedAgent.tools as tool}
						<li>{tool}</li>
					{/each}
				</ul>
				<div>
					model: <br />
					{displayedAgent.model}
				</div>
			</div>
		</Dialog.Content>
	</Dialog.Root>
</div>
