<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { createEventDispatcher } from 'svelte';
	import type { Agent, Crew } from '$lib/types/models';
	import { AgentItems, CrewItems } from '$lib/components/ui/community-details';

	export let type: 'agent' | 'crew';
	export let displayedItem: Agent | Crew;
	export let showDetails: boolean;

	const dispatch = createEventDispatcher();

	function closeDialog() {
		dispatch('close');
		showDetails = false;
	}

	$: agentItem = <Agent>displayedItem;
	$: crewItem = <Crew>displayedItem;
</script>

<Dialog.Root open={showDetails} onOpenChange={() => closeDialog()}>
	<Dialog.Content
		class={type === 'agent'
			? 'h-5/6 w-full max-w-6xl space-y-8 overflow-y-auto rounded-lg p-8 shadow-2xl [&::-webkit-scrollbar]:hidden'
			: 'relative max-w-5xl transform rounded-xl bg-background p-8 shadow-xl transition-all duration-500 ease-in-out hover:scale-105'}
	>
		{#if type === 'agent'}
			<AgentItems agentDisplayDetails={agentItem} />
		{:else}
			<CrewItems crewDisplayDetails={crewItem} />
		{/if}
	</Dialog.Content>
</Dialog.Root>
