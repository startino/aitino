<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import * as Card from '$lib/components/ui/card';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import { fade } from 'svelte/transition';
	import * as Dialog from '$lib/components/ui/dialog';
	import type { Agent } from '$lib/types/models';

	export let myAgents: Agent[];
	export let publishedAgents: Agent[];

	let searchQuery = '';
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

	$: filteredMyAgents = myAgents.filter(
		(a) =>
			(searchQuery === '' ||
				a.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.description.some((desc) => desc.toLowerCase().includes(searchQuery.toLowerCase()))) &&
			(!filterPublished || a.published) &&
			(filterModel === '' || a.model === filterModel)
	);

	$: showNoResults = filteredMyAgents.length === 0 && searchQuery !== '';
	$: filteredPublishedAgents = publishedAgents.filter(
		(a) =>
			(searchQuery === '' ||
				a.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
				a.description.some((desc) => desc.toLowerCase().includes(searchQuery.toLowerCase()))) &&
			(!filterPublished || a.published) &&
			(filterModel === '' || a.model === filterModel)
	);

	$: showNoResultsForPublished = filteredMyAgents.length === 0 && searchQuery !== '';

	let showDetails = false;
	let displayedAgent: Agent;
	let showDetailInTheModal = async (id: string) => {
		displayedAgent = myAgents.find((a) => a.id === id) || publishedAgents.find((a) => a.id === id);
		console.log(displayedAgent, 'new Agent');
	};

	function timeSince(dateIsoString: Date | string) {
		const date = new Date(dateIsoString);
		const now = new Date();
		const diffInSeconds = Math.round((now - date) / 1000);

		console.log(diffInSeconds, 'diffInSeconds \n', now, 'now \n', date, 'date');

		if (diffInSeconds < 60) {
			return 'just now';
		} else if (diffInSeconds < 3600) {
			return `${Math.floor(diffInSeconds / 60)} minutes ago`;
		} else if (diffInSeconds < 86400) {
			return `${Math.floor(diffInSeconds / 3600)} hours ago`;
		} else if (diffInSeconds < 172800) {
			return 'yesterday';
		} else {
			return `${Math.floor(diffInSeconds / 86400)} days ago`;
		}
	}
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
			{#each filteredMyAgents as agent}
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
									<img
										src={agent.avatar_url}
										alt={agent.name}
										class="border-primary rounded-full border-4 object-cover shadow-2xl"
									/>
								</div>
								<div class="flex flex-col">
									<div
										class="bg-gradient-to-r from-green-200 to-teal-300 bg-clip-text text-2xl font-extrabold text-transparent"
									>
										{agent.name}
									</div>
									<div class="text-lg italic text-gray-500">{agent.author}</div>
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
								{#if agent.updated_at !== null}
									<div class="justify-self-end">{timeSince(agent.updated_at)}</div>{/if}
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
			{#each filteredPublishedAgents as agent}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div
					class="cursor-pointer hover:scale-[101%]"
					transition:fade={{ delay: 500, duration: 400 }}
					on:click={() => ((showDetails = true), showDetailInTheModal(agent.id))}
				>
					<Card.Root>
						<div class="flex items-center justify-between px-6">
							<div class="z-50 flex gap-4 gap-y-4 p-4">
								<div class="flex h-20 w-20 items-center justify-center rounded-full border">
									<img
										src={agent.avatar_url}
										alt={agent.name}
										class="border-primary rounded-full border-4 object-cover shadow-2xl"
									/>
								</div>
								<div class="flex flex-col">
									<div
										class="bg-gradient-to-r from-green-200 to-teal-300 bg-clip-text text-2xl font-extrabold text-transparent"
									>
										{agent.name}
									</div>
									<div class="text-lg italic text-gray-500">{agent.author}</div>
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
								{#if agent.updated_at !== null}
									<div class="justify-self-end">{timeSince(agent.updated_at)}</div>{/if}
							</div>
						</Card.Content>
					</Card.Root>
				</div>
			{/each}
			{#if showNoResultsForPublished}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>
	</Tabs.Root>
</div>

<div class="mx-auto w-full max-w-6xl">
	<Dialog.Root open={showDetails} onOpenChange={() => (showDetails = false)}>
		<Dialog.Content
			class="h-5/6 w-full max-w-6xl space-y-8 overflow-y-auto rounded-lg p-8 shadow-2xl [&::-webkit-scrollbar]:hidden"
		>
			<div class="mb-8 flex flex-col items-center justify-center">
				<div class="relative">
					<img
						src={displayedAgent.avatar_url}
						alt={displayedAgent.name}
						class="border-primary h-48 w-48 rounded-full border-4 object-cover shadow-2xl"
					/>
					<div
						class="absolute -bottom-2 -right-2 animate-pulse rounded-full bg-blue-500 px-3 py-2 text-xs font-semibold text-white"
					>
						V {displayedAgent.version}
					</div>
				</div>
				<div class="mt-4 flex flex-col items-center">
					{#if displayedAgent.created_at}
						<p class="text-sm text-gray-400">Created {timeSince(displayedAgent.created_at)}</p>
					{/if}
					<!-- Enhanced Model info with badge-like component -->
					<div
						class="mt-2 inline-flex items-center justify-center rounded-full bg-green-500 px-3 py-1 text-xs font-semibold text-white shadow"
					>
						Model: {displayedAgent.model}
					</div>
				</div>
			</div>
			<div class="space-y-4 text-center">
				<h2
					class="bg-gradient-to-r from-blue-400 to-teal-300 bg-clip-text py-2 text-6xl font-extrabold text-transparent"
				>
					{displayedAgent.name}
				</h2>
				<p class="mx-auto max-w-3xl text-xl text-gray-400">{displayedAgent.summary}</p>
				<p class="text-lg italic text-gray-500">— {displayedAgent.author}</p>
				{#if displayedAgent.updated_at !== null}
					<p class="text-sm text-gray-400">Updated {timeSince(displayedAgent.updated_at)}</p>
				{/if}
			</div>

			<div class="text-white">
				<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Description</h3>
				<ul class="mt-4 list-inside list-disc space-y-2 text-gray-400">
					{#each displayedAgent.description as description}
						<li>{description}</li>
					{/each}
				</ul>
			</div>

			<div class="mt-6 text-white">
				<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Tools</h3>
				<div class="mt-4 flex flex-wrap gap-2">
					{#each displayedAgent.tools as tool}
						<span
							class="rounded-full bg-gray-700 px-4 py-2 text-sm transition-colors duration-200 hover:bg-gray-600"
							>{tool}</span
						>
					{/each}
				</div>
			</div>
		</Dialog.Content>
	</Dialog.Root>
</div>
