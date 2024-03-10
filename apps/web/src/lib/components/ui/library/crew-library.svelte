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
	import { LibraryDetails } from '$lib/components/ui/community-details';

	const dispatch = createEventDispatcher();

	export let myCrews: Crew[];
	export let publishedCrews: Crew[];

	let searchQuery = '';
	let filterPublished = false;
	let filterModel = '';
	let showDetails = false;
	let displayedAgent: Crew;

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
		displayedAgent = myCrews.find((a) => a.id === id) || publishedCrews.find((a) => a.id === id);
	};

	function handleClose() {
		showDetails = false;
	}

	const reusableClasses = {
		tabContent_content:
			'h-4/6 max-h-[700px] space-y-7 overflow-y-scroll [&::-webkit-scrollbar]:hidden',
		scale_on_hover: 'cursor-pointer hover:scale-[101%]',
		image_parent_class: 'g-primary-200 flex h-20 w-20 items-center justify-center rounded-full p-1',
		agent_title:
			'bg-gradient-to-r from-green-200 to-teal-300 bg-clip-text text-2xl font-extrabold text-transparent',
		button_class:
			'ring-offset-background focus-visible:ring-ring bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground inline-flex h-10 max-w-xs items-center justify-center whitespace-nowrap rounded-md px-12 py-2 text-sm font-bold transition-colors hover:scale-[98%] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
		card_class: 'flex items-center justify-between px-6'
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
		<Tabs.Content value="personal" class={reusableClasses.tabContent_content}>
			{#each filteredMyCrews as agent}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div
					class={reusableClasses.scale_on_hover}
					transition:fade={{ delay: 500, duration: 400 }}
					on:click={() => ((showDetails = true), showDetailInTheModal(agent.id))}
				>
					<Card.Root>
						<div class={reusableClasses.card_class}>
							<div class="flex gap-4 gap-y-4 p-4">
								<div class={reusableClasses.image_parent_class}>
									<img
										src={agent.avatar}
										alt={agent.title}
										class="rounded-full border-4 object-cover shadow-2xl"
									/>
								</div>
								<div class="flex flex-col">
									<div class={reusableClasses.agent_title}>
										{agent.title}
									</div>
								</div>
							</div>
							<div class="flex h-full items-center justify-between">
								<Button variant="ghost" class="text-foreground max-w-xs  px-12 hover:bg-transparent"
									>see more</Button
								>
								<button
									class={reusableClasses.button_class}
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
							<div class="{reusableClasses.card_class} px-0">
								<p class="max-w-4xl px-6">
									{agent.description}
								</p>
							</div>
						</Card.Content>
					</Card.Root>
				</div>
			{/each}
			{#if showNoResults}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>

		<Tabs.Content value="community" class={reusableClasses.tabContent_content}>
			{#each filteredPublishedCrews as agent}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div
					class={reusableClasses.scale_on_hover}
					transition:fade={{ delay: 500, duration: 400 }}
					on:click={() => ((showDetails = true), showDetailInTheModal(agent.id))}
				>
					<Card.Root>
						<div class={reusableClasses.card_class}>
							<div class="z-50 flex gap-4 gap-y-4 p-4">
								<div class={reusableClasses.image_parent_class}>
									<img
										src={agent.avatar}
										alt={agent.title}
										class="rounded-full object-cover shadow-2xl"
									/>
								</div>
								<div class="flex flex-col">
									<div class={reusableClasses.agent_title}>
										{agent.title}
									</div>
								</div>
							</div>
							<div class="{reusableClasses.card_class} px-0">
								<Button variant="ghost" class="text-foreground max-w-xs px-12 hover:bg-transparent"
									>see more</Button
								>
								<button
									class={reusableClasses.button_class}
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

<LibraryDetails type="crew" {displayedAgent} {showDetails} on:close={handleClose} />
