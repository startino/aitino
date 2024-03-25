<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Label } from '$lib/components/ui/label';
	import type { Crew } from '$lib/types/models';
	import { Library } from '$lib/components/ui/community-details';
	import CrewRow from '../community-details/crew-row.svelte';

	const dispatch = createEventDispatcher();

	export let myCrews: Crew[];
	export let publishedCrews: Crew[];

	let searchQuery = '';
	let filterPublished = false;
	let filterModel = '';
	let showDetails = false;
	let displayedCrew: Crew;

	// filter the personal crews based on search query
	$: filteredCrews = (crews: Crew[]) => {
		return crews.filter(
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
	};

	$: filteredMyCrews = filteredCrews(myCrews);
	$: filteredPublishedCrews = filteredCrews(publishedCrews);

	// show no results message for the personal crews based on search query
	$: showNoResults = filteredMyCrews.length === 0 && searchQuery !== '';

	// show no results message for the published crews based on search query
	$: showNoResultsForPublished = filteredPublishedCrews.length === 0 && searchQuery !== '';

	// update the search query based on user input
	function updateSearchQuery(event: Event) {
		const input = event.target as HTMLInputElement;
		searchQuery = input.value.toLowerCase();
	}

	// toggle the published filter based on user selection
	function togglePublished() {
		filterPublished = !filterPublished;
	}

	//  shows the detail of the current crew
	let showDetailInTheModal = async (id: string) => {
		displayedCrew = myCrews.find((a) => a.id === id) || publishedCrews.find((a) => a.id === id);
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
					</DropdownMenu.Content>
				</DropdownMenu.Root>
			</div>
			<form
				method="POST"
				class="grid grid-cols-8 items-center rounded-md border border-border bg-card p-6"
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
				<div class="col-span-7 flex flex-col justify-center gap-2 align-middle">
					<label for="file_input" class="mb-2 text-sm font-medium"> Upload a Crew </label>
					<input
						class="file:bg-foreground-50 block w-full cursor-pointer rounded-md border file:mr-4 file:rounded-sm file:border-0 file:px-4 file:py-2 file:text-base file:font-semibold"
						id="file_input"
						type="file"
						accept=".json"
					/>
				</div>
				<div class="col-span-1 ml-auto flex h-full items-end justify-end">
					<Button variant="outline" type="submit">Load</Button>
				</div>
			</form>
		</div>
		<Tabs.Content
			value="personal"
			class="h-4/6 max-h-[700px] space-y-7 overflow-y-scroll [&::-webkit-scrollbar]:hidden"
		>
			{#each filteredMyCrews as crew}
				<CrewRow
					{crew}
					on:click={({ detail }) => ((showDetails = true), showDetailInTheModal(detail.id))}
					on:load={({ detail }) => {
						dispatch('crewLoad', {
							id: detail.receiver_id,
							title: detail.title,
							nodes: detail.nodes,
							edges: detail.edges,
							description: detail.description
						});
					}}
				/>
			{/each}
			{#if showNoResults}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>

		<Tabs.Content
			value="community"
			class="h-4/6 max-h-[700px] space-y-7 overflow-y-scroll [&::-webkit-scrollbar]:hidden"
		>
			{#each filteredPublishedCrews as crew}
				<CrewRow
					{crew}
					on:click={({ detail }) => ((showDetails = true), showDetailInTheModal(detail.id))}
					on:load={({ detail }) => {
						dispatch('crewLoad', {
							id: detail.receiver_id,
							title: detail.title,
							nodes: detail.nodes,
							edges: detail.edges,
							description: detail.description
						});
					}}
				/>
			{/each}
			{#if showNoResultsForPublished}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>
	</Tabs.Root>
</div>

<Library type="crew" displayedItem={displayedCrew} {showDetails} on:close={handleClose} />
