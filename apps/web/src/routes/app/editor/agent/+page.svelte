<script lang="ts">
	import { ComingSoonPage } from '$lib/components/ui/coming-soon';
	import { CreateAgent, EditAgent } from '$lib/components/ui/agent-editor/';
	import type { Agent } from '$lib/types/models';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Loader2 } from 'lucide-svelte';
	import { applyAction, enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { Toggle } from '$lib/components/ui/toggle/index.js';
	import { message } from 'sveltekit-superforms/server';

	let state: 'loading' | 'error' | 'idle' = 'idle';
	export let data;
	export let form;

	let myAgents: Agent[] = data.getCurrentUserAgents.data;

	let open = false;

	let selectedAgent: Agent;

	const editAgent = async (agent: Agent) => {
		console.log(agent, 'agent');
		selectedAgent = agent;
		open = true;
	};

	let published = false;
	const handleClose = () => {
		open = false;

		console.log('handle ', open);
	};
</script>

<div class="bg-background min-h-screen p-8">
	<h1 class="text-primary dark:text-primary/80 mb-8 text-center text-4xl font-bold">
		<span class="from-accent to-secondary bg-gradient-to-r bg-clip-text text-transparent"
			>My Agent</span
		>
	</h1>
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		{#each myAgents as agent}
			<div
				class="bg-surface group relative flex flex-col overflow-hidden rounded-lg shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<div class="flex-shrink-0">
					<img
						src={agent.avatar}
						alt={`Avatar of ${agent.title}`}
						class="h-48 w-full object-cover transition-transform duration-500 group-hover:scale-110"
					/>
				</div>
				<div class="flex flex-grow flex-col p-4">
					<div class="flex justify-between">
						<h3 class="text-on-surface text-lg font-semibold">{agent.title}</h3>
					</div>
					<p class="text-on-surface/80 mt-2 flex-grow text-sm">{agent.role}</p>
				</div>
				<button
					class="bg-primary text-background hover:bg-primary/90 text-md mt-4 w-full rounded-none p-2 font-semibold transition-colors duration-300"
					on:click={() => {
						open = true;
						editAgent(agent);
					}}>Edit Agent</button
				>
			</div>
		{/each}
	</div>
</div>

{#if form?.message}
	<p>{form?.message}</p>
{/if}
<!-- <ComingSoonPage releaseVersion="v0.3.0" /> -->
<CreateAgent on:close={() => (open = false)} {form} data={data.agentForm} />

<EditAgent {selectedAgent} on:close={handleClose} {open} {form} message={form?.message} />
