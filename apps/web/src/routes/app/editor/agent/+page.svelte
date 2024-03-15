<script lang="ts">
	import { writable } from 'svelte/store';
	import { afterUpdate, onMount } from 'svelte';
	import { CreateAgent, EditAgent} from '$lib/components/ui/agent-editor';
	import type { Agent } from '$lib/types/models';
  
	// Assuming `data` and `form` are passed as props to this component
	export let data;
	export let form;
  
	let myAgents: Agent[] = [];
	const selectedAgent = writable<Agent | null>(null);
	let open = false;
  
	myAgents = data.getCurrentUserAgents.data;
	afterUpdate(async () => {
	  myAgents = data.getCurrentUserAgents.data;
	});
  
	function editAgent(agent: Agent) {
	  selectedAgent.set(agent);
	  open = true;
	}
  
	function handleClose() {
	  open = false;
	  // Reset selected agent after closing the modal to allow reopening for another agent
	  selectedAgent.set(null);
	}
  </script>
  
  <CreateAgent on:close={() => (open = false)} {form} data={data.agentForm} />
  
  <div class="bg-background min-h-screen p-8">
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
	  {#each myAgents as agent}
		<div class="bg-surface group relative flex flex-col overflow-hidden rounded-lg shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl">
		  <div class="flex-shrink-0">
			<img src={agent.avatar} alt={`Avatar of ${agent.title}`} class="h-48 w-full object-cover transition-transform duration-500 group-hover:scale-110" />
		  </div>
		  <div class="flex flex-grow flex-col p-4">
			<h3 class="text-on-surface text-lg font-semibold">{agent.title}</h3>
			<p class="text-on-surface/80 mt-2 flex-grow text-sm">{agent.role}</p>
		  </div>
		  <button class="bg-primary text-background hover:bg-primary/90 text-md mt-4 w-full rounded-none p-2 font-semibold transition-colors duration-300" on:click={() => editAgent(agent)}>
			Edit Agent
		  </button>
		</div>
	  {/each}
	</div>
  </div>
  
  <EditAgent selectedAgent={$selectedAgent} open={open} on:close={handleClose} {form} />
  