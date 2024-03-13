<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import type { Crew } from '$lib/types/models';
	import * as Card from '$lib/components/ui/card';
	import { fade } from 'svelte/transition';
	import { User, User2 } from 'lucide-svelte';
	import CrewLibraryDetails from '../community-details/crewLibraryDetails.svelte';
	import LibraryDetails from '../community-details/libraryDetails.svelte';

	const dispatch = createEventDispatcher();

	export let myCrews: Crew[];
	export let publishedCrews: Crew[];

	let searchQuery = '';
	let filterPublished = false;
	let filterModel = '';
	let showDetails = false;
	let displayedAgent: Crew;

	function updateSearchQuery(event: Event) {
		const input = event.target as HTMLInputElement;
		searchQuery = input.value.toLowerCase();
	}

	function togglePublished() {
		filterPublished = !filterPublished;
	}

	function updateFilterModel(model: string) {
		filterModel = filterModel === model ? '' : model;
	}

	// Adjusted filtering logic for myCrews and publishedCrews
	$: filteredMyCrews = myCrews.filter(
		(crew) =>
			searchQuery === '' ||
			crew.description.toLowerCase().includes(searchQuery) ||
			(crew.nodes.some(
				(node) =>
					(node.data.name?.toLowerCase() ?? '').includes(searchQuery) ||
					(node.data.description?.toLowerCase() ?? '').includes(searchQuery) ||
					(node.data.model?.label?.toLowerCase() ?? '').includes(searchQuery)
			) &&
				(!filterPublished || crew.published) &&
				(filterModel === '' || crew.nodes.some((node) => node.data.model?.label === filterModel)))
	);

	$: filteredPublishedCrews = publishedCrews.filter(
		(crew) =>
			searchQuery === '' ||
			crew.description.toLowerCase().includes(searchQuery) ||
			(crew.nodes.some(
				(node) =>
					(node.data.name?.toLowerCase() ?? '').includes(searchQuery) ||
					(node.data.description?.toLowerCase() ?? '').includes(searchQuery) ||
					(node.data.model?.label?.toLowerCase() ?? '').includes(searchQuery)
			) &&
				(!filterPublished || crew.published) &&
				(filterModel === '' || crew.nodes.some((node) => node.data.model?.label === filterModel)))
	);

	$: showNoResults = filteredMyCrews.length === 0 && searchQuery !== '';

	$: showNoResultsForPublished = filteredPublishedCrews.length === 0 && searchQuery !== '';

	let showDetailInTheModal = async (id: string) => {
		displayedAgent = myCrews.find((a) => a.id === id) || publishedCrews.find((a) => a.id === id);
		console.log(displayedAgent);
	};

	function handleClose() {
		showDetails = false;
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
					bind:value={searchQuery}
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
						<!-- <DropdownMenu.CheckboxItem
							checked={filterModel === 'gpt-3'}
							on:click={() => updateFilterModel('gpt-3')}
						>
							GPT-3
						</DropdownMenu.CheckboxItem>
						<DropdownMenu.CheckboxItem
							checked={filterModel === 'gpt-3.5 turbo'}
							on:click={() => updateFilterModel('gpt-3.5 turbo')}
						>
							GPT-3.5 Turbo
						</DropdownMenu.CheckboxItem>
						<DropdownMenu.CheckboxItem
							checked={filterModel === 'gpt-4'}
							on:click={() => updateFilterModel('gpt-4')}
						>
							GPT-4
						</DropdownMenu.CheckboxItem> -->
					</DropdownMenu.Content>
				</DropdownMenu.Root>
			</div>
			<form
				method="POST"
				class="border-border bg-card grid grid-cols-8 rounded-md border p-6"
				on:submit|preventDefault={async (e) => {
					const file = e.target[0].files[0];

					if (!file) return;

					try {
						const text = await file.text();
						dispatch('crew-load', {
							crew: JSON.parse(text)
						});
					} catch (error) {
						console.error('Error parsing JSON:', error);
					}
				}}
			>
				<div class="col-span-7 grid w-full max-w-sm items-center gap-1.5">
					<Label for="file">Upload a Crew from a file with the button below</Label>

					<Input
						id="file"
						accept=".json"
						type="file"
						class="border-border bg-foreground/10 border"
					/>
				</div>
				<div class="col-span-1 ml-auto">
					<Button variant="outline" type="submit">Load</Button>
				</div>
			</form>
		</div>
		<Tabs.Content
			value="personal"
			class="h-5/6 space-y-6 overflow-y-scroll [&::-webkit-scrollbar]:hidden"
		>
			{#each filteredMyCrews as agent}
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
								<div class="flex h-20 w-20 items-center justify-center rounded-full">
									<!-- <img
										src={agent.avatar}
										alt={agent.name}
										class="border-primary rounded-full border-4 object-cover shadow-2xl"
									/> -->
									<div class="bg-primary-200 rounded-full p-1">
										<div class="bg-background rounded-full p-2">
											<User class="text-primary-500 h-12 w-12" />
										</div>
									</div>
								</div>
								<div class="flex flex-col">
									<div
										class="bg-gradient-to-r from-green-200 to-teal-300 bg-clip-text text-2xl font-extrabold text-transparent"
									>
										{agent.title}
									</div>
									<!-- <div class="text-lg italic text-gray-500">{agent.}</div> -->
								</div>
							</div>
							<div class="flex h-full items-center justify-between">
								<Button variant="ghost" class="text-foreground max-w-xs  px-12 hover:bg-transparent"
									>see more</Button
								>
								<button
									class="ring-offset-background focus-visible:ring-ring bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground inline-flex h-10 max-w-xs items-center justify-center whitespace-nowrap rounded-md px-12 py-2 text-sm font-bold transition-colors hover:scale-[98%] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
									on:click|stopPropagation={() =>
										dispatch('crewLoad', {
											id: agent.receiver_id,
											title: agent.title,
											nodes: agent.nodes,
											edges: agent.edges,
											description: agent.description
										})}>Load</button
								>
							</div>
						</div>
						<Card.Content>
							<div class="flex justify-between">
								<p class="max-w-4xl px-6">
									{agent.description}
								</p>
								<!-- {#if agent.updated_at !== null}
									<div class="justify-self-end">{timeSince(agent.updated_at)}</div>{/if} -->
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
			{#each filteredPublishedCrews as agent}
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
								<div class="flex h-20 w-20 items-center justify-center rounded-full">
									<!-- <img
										src={agent.avatar}
										alt={agent.name}
										class="border-primary rounded-full border-4 object-cover shadow-2xl"
									/> -->
									<div class="bg-primary-200 rounded-full p-1">
										<div class="bg-background rounded-full p-2">
											<User class="text-primary-500 h-12 w-12" />
										</div>
									</div>
								</div>
								<div class="flex flex-col">
									<div
										class="bg-gradient-to-r from-green-200 to-teal-300 bg-clip-text text-2xl font-extrabold text-transparent"
									>
										{agent.title}
									</div>
									<!-- <div class="text-lg italic text-gray-500">{agent.author}</div> -->
								</div>
							</div>
							<div class="flex h-full items-center justify-between">
								<Button variant="ghost" class="text-foreground max-w-xs px-12 hover:bg-transparent"
									>see more</Button
								>
								<button
									class="ring-offset-background focus-visible:ring-ring bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground inline-flex h-10 max-w-xs items-center justify-center whitespace-nowrap rounded-md px-12 py-2 text-sm font-bold transition-colors hover:scale-[98%] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
									on:click|stopPropagation={() =>
										dispatch('crewLoad', {
											id: agent.receiver_id,
											title: agent.title,
											nodes: agent.nodes,
											edges: agent.edges,
											description: agent.description
										})}>Load</button
								>
							</div>
						</div>
						<Card.Content>
							<div class="flex justify-between" on:click={() => (showDetails = true)}>
								<p class="max-w-4xl px-6">
									{agent.description}
								</p>
								<!-- {#if agent.updated_at !== null}
									<div class="justify-self-end">{timeSince(agent.updated_at)}</div>{/if} -->
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

<!-- <CrewLibraryDetails {displayedAgent} {showDetails} on:close={handleClose} /> -->
<LibraryDetails type="crew" {displayedAgent} {showDetails} on:close={handleClose} />
