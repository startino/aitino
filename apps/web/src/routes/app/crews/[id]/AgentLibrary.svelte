<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import ChevronDown from 'lucide-svelte/icons/chevron-down';
	import { createEventDispatcher } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { Library } from '$lib/components/ui/community-details';
	import AgentRow from '$lib/components/ui/community-details/agent-row.svelte';
	import type { schemas } from '$lib/api';
	import { getContext } from '$lib/utils';
	import { useSvelteFlow } from '@xyflow/svelte';
	import { AGENT_LIMIT } from '$lib/config';

	let { crew, agents, publishedAgents, nodes } = getContext('crew');

	let searchQuery = '';
	let filterPublished = false;
	let filterModel = '';
	let showDetails = false;
	let displayedAgent: schemas['Agent'];

	// filter the agents based on the search query
	$: filterAgents = (agents: schemas['Agent'][]) => {
		return agents.filter(
			(agent) =>
				(searchQuery === '' ||
					agent.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
					agent.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
					agent.description.toLowerCase().toLowerCase().includes(searchQuery.toLowerCase())) &&
				(!filterPublished || agent.published) &&
				(filterModel === '' || agent.model === filterModel)
		);
	};

	$: filteredAgents = filterAgents($agents);

	$: filteredPublishedAgents = filterAgents($publishedAgents);
	$: showNoResults = filteredAgents.length === 0 && searchQuery !== '';
	$: showNoResultsForPublished = filteredPublishedAgents.length === 0 && searchQuery !== '';

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

	function handleClose() {
		showDetails = false;
	}

	const { getViewport } = useSvelteFlow();
	const addAgent = async (agent: schemas['Agent']) => {
		if ($nodes.length >= AGENT_LIMIT) {
			toast.error(`You have reached the maximum limit of ${AGENT_LIMIT} agents.`);
			return;
		}

		if ($nodes.find((node) => node.id === agent.id)) {
			toast.error(
				`Agent is already in the crew. We are working on supporting multiple of the same agent...`
			);
			return;
		}

		const position = { ...getViewport() };

		nodes.update((v) => [
			...v,
			{
				id: agent.id,
				type: 'agent',
				selectable: false,
				position,
				data: {}
			}
		]);
		toast.success(`Added a new agent ${agent.title}`);
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
							checked={filterModel === 'gpt-3.5-turbo'}
							on:click={() => updateFilterModel('gpt-3.5-turbo')}
						>
							GPT-3.5-turbo
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
		<Tabs.Content
			value="personal"
			class="h-5/6 space-y-6 overflow-y-scroll [&::-webkit-scrollbar]:hidden"
		>
			{#each filteredAgents as agent, index (`personal-${agent.id}`)}
				<AgentRow
					{agent}
					on:click={({ detail: agent }) => {
						showDetails = true;
						displayedAgent = agent;
					}}
					on:load={({ detail: agent }) => {
						addAgent(agent);
					}}
				/>
			{/each}
			{#if showNoResults}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>

		<Tabs.Content
			value="community"
			class="h-5/6 space-y-6 overflow-y-scroll [&::-webkit-scrollbar]:hidden"
		>
			{#each filteredPublishedAgents as agent, index (`community-${agent.id}`)}
				<AgentRow
					{agent}
					on:click={({ detail: agent }) => {
						showDetails = true;
						displayedAgent = agent;
					}}
					on:load={({ detail: agent }) => {
						addAgent(agent);
					}}
				/>
			{/each}
			{#if showNoResultsForPublished}
				<div class="no-results">No search results found</div>
			{/if}
		</Tabs.Content>
	</Tabs.Root>
</div>

<!-- component to show details of the current agent  -->
<Library type="agent" displayedItem={displayedAgent} {showDetails} on:close={handleClose} />
