<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { createEventDispatcher } from 'svelte';
	import type { Agent, Crew } from '$lib/types/models';
	import { AgentDetails, CrewDetails } from '$lib/components/ui/community-details';

	export let type: 'agent' | 'crew';
	export let displayedAgent: Agent | Crew
	export let showDetails: boolean;

	const dispatch = createEventDispatcher();

	function closeDialog() {
		dispatch('close');
		showDetails = false;
	}

	$: isAgent = type === 'agent';
	$: agentItem = isAgent ? <Agent>displayedAgent : null;
	$: crewItem = !isAgent ? <Crew>displayedAgent : null;
</script>

<Dialog.Root open={showDetails} onOpenChange={() => closeDialog()}>
	<Dialog.Content
		class={type === 'agent'
			? 'h-5/6 w-full max-w-6xl space-y-8 overflow-y-auto rounded-lg p-8 shadow-2xl [&::-webkit-scrollbar]:hidden'
			: 'relativ bg-background max-w-5xl transform rounded-xl p-8 shadow-xl transition-all duration-500 ease-in-out hover:scale-105'}
	>
		{#if type === 'agent'}
			<AgentDetails AgentDisplayDetails={agentItem} />
		{:else}
			<CrewDetails CrewDisplayDetails={crewItem} />
		{/if}
	</Dialog.Content>
</Dialog.Root>
