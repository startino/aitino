<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import * as Card from '$lib/components/ui/card';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import { fade } from 'svelte/transition';
	import type { Agent } from '$lib/types/models';
	import { createEventDispatcher } from 'svelte';
	import { toast } from 'svelte-sonner';
	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';
	import { LibraryDetails } from '$lib/components/ui/community-details';

	const dispatch = createEventDispatcher();

	export let myAgents: Agent[];
	export let publishedAgents: Agent[];

	let searchQuery = '';
	let filterPublished = false;
	let filterModel = '';
	let showDetails = false;
	let displayedAgent: Agent;

	dayjs.extend(relativeTime);

	// filter the agents based on the search query
	$: filterAgents = (agents: Agent[]) => {
		return agents.filter(
			(agent) =>
				(searchQuery === '' ||
					agent.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
					agent.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
					agent.description.some((desc) =>
						desc.toLowerCase().includes(searchQuery.toLowerCase())
					)) &&
				(!filterPublished || agent.published) &&
				(filterModel === '' || agent.model === filterModel)
		);
	};

	$: filteredMyAgents = filterAgents(myAgents);

	$: filteredPublishedAgents = filterAgents(publishedAgents);
	$: showNoResults = filteredMyAgents.length === 0 && searchQuery !== '';
	$: showNoResultsForPublished = filteredPublishedAgents.length === 0 && searchQuery !== '';

	// funtion to show details of the current agent
	let showDetailInTheModal = async (id: string) => {
		displayedAgent = myAgents.find((a) => a.id === id) || publishedAgents.find((a) => a.id === id);
	};

	// update the search query based on user input
	function updateSearchQuery(event: Event) {
		const input = event.target as HTMLInputElement;
		searchQuery = input.value;
	}

	// toggle the filter for published
	function togglePublished() {
		filterPublished = !filterPublished;
	}

	// update the filter model based on user selection
	function updateFilterModel(model: string) {
		filterModel = model !== filterModel ? model : '';
	}

	// function to filter the date
	function timeSince(dateIsoString: Date | string | number | undefined) {
		return dayjs(dateIsoString).fromNow(true);
	}

	function handleClose() {
		showDetails = false;
	}

	const reusableClasses = {
		tabContent_Class: 'h-5/6 space-y-6 overflow-y-scroll [&::-webkit-scrollbar]:hidden',
		scale_on_hover: 'cursor-pointer hover:scale-[101%]',
		image_class: 'border-primary rounded-full border-4 object-cover shadow-2xl',
		image_parent_class: 'flex h-20 w-20 items-center justify-center rounded-full',
		agent_title:
			'bg-gradient-to-r from-green-200 to-teal-300 bg-clip-text text-2xl font-extrabold text-transparent',
		button_class:
			'ring-offset-background focus-visible:ring-ring bg-primary text-primary-foreground hover:bg-accent hover:text-accent-foreground inline-flex h-10 max-w-xs items-center justify-center whitespace-nowrap rounded-md px-12 py-2 text-sm font-bold transition-colors hover:scale-[98%] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
		card_root: 'flex items-center justify-between px-6',
		ghost_button: 'text-foreground max-w-xs px-12 hover:bg-transparent'
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
							checked={filterModel === 'gpt-3-turbo'}
							on:click={() => updateFilterModel('gpt-3-turbo')}
						>
							GPT-3
						</DropdownMenu.CheckboxItem>
						<DropdownMenu.CheckboxItem
							checked={filterModel === 'gpt-4-turbo-preview'}
							on:click={() => updateFilterModel('gpt-4-turbo-preview')}
						>
							GPT-4
						</DropdownMenu.CheckboxItem>
					</DropdownMenu.Content>
				</DropdownMenu.Root>
			</div>
		</div>
		<Tabs.Content value="personal" class={reusableClasses.tabContent_Class}>
			{#each filteredMyAgents as agent, index (`personal-${agent.id}`)}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div
					class={reusableClasses.scale_on_hover}
					transition:fade={{ delay: 500, duration: 400 }}
					on:click={() => ((showDetails = true), showDetailInTheModal(agent.id))}
				>
					<Card.Root>
						<div class={reusableClasses.card_root}>
							<div class="flex gap-4 gap-y-4 p-4">
								<div class={reusableClasses.image_parent_class}>
									<img src={agent.avatar} alt={agent.title} class={reusableClasses.image_class} />
								</div>
								<div class="flex flex-col">
									<div class={reusableClasses.agent_title}>
										{agent.title}
									</div>
								</div>
							</div>
							<div class="{reusableClasses.card_root} h-full px-0">
								<Button variant="ghost" class={reusableClasses.ghost_button}>see more</Button>
								<button
									class={reusableClasses.button_class}
									on:click|stopPropagation={() => {
										toast.success(`Added a new agent ${agent.title}`);
										dispatch('loadAgent', {
											name: agent.title,
											model: agent.model,
											job: agent.role,
											avatar: agent.avatar
										});
									}}
								>
									Load
								</button>
							</div>
						</div>
						<Card.Content>
							<div class="flex justify-between">
								<p class="max-w-4xl px-6">
									{agent.role}
								</p>
								<div class="justify-self-end">{timeSince(agent.created_at)}</div>
							</div>
						</Card.Content>
					</Card.Root>
				</div>
			{/each}
			{#if showNoResults}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>

		<Tabs.Content value="community" class={reusableClasses.tabContent_Class}>
			{#each filteredPublishedAgents as agent, index (`community-${agent.id}`)}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div
					class={reusableClasses.scale_on_hover}
					transition:fade={{ delay: 500, duration: 400 }}
					on:click={() => ((showDetails = true), showDetailInTheModal(agent.id))}
				>
					<Card.Root>
						<div class={reusableClasses.card_root}>
							<div class="z-50 flex gap-4 gap-y-4 p-4">
								<div class={reusableClasses.image_parent_class}>
									<img src={agent.avatar} alt={agent.title} class={reusableClasses.image_class} />
								</div>
								<div class="flex flex-col">
									<div class={reusableClasses.agent_title}>
										{agent.title}
									</div>
								</div>
							</div>
							<div class=" {reusableClasses.card_root} h-full px-0">
								<Button variant="ghost" class={reusableClasses.ghost_button}>see more</Button>
								<button
									class={reusableClasses.button_class}
									on:click|stopPropagation={(event) => {
										toast.success(`Added a new agent from the community: ${agent.title}`);
										dispatch('loadAgent', {
											id: agent.id,
											name: agent.title,
											model: agent.model,
											job: agent.role,
											avatar: agent.avatar
										});
									}}>Load</button
								>
							</div>
						</div>
						<Card.Content>
							<div class="flex justify-between" on:click={() => (showDetails = true)}>
								<p class="max-w-4xl px-6">
									{agent.role}
								</p>
								<div class="justify-self-end">{timeSince(agent?.created_at)}</div>
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

<!-- component to show details of the current agent  -->
<LibraryDetails type="agent" {displayedAgent} {showDetails} on:close={handleClose} />
