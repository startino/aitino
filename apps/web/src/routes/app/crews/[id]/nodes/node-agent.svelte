<script lang="ts">
	import { type NodeProps, useSvelteFlow } from '@xyflow/svelte';
	import { X } from 'lucide-svelte';

	// 👇 always import the styles
	import '@xyflow/svelte/dist/style.css';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { getContext } from '$lib/context';

	const { agents, publishedAgents } = getContext('root');

	type $$Props = NodeProps;

	export let id: NodeProps['id'];

	const agent = [...$agents, ...$publishedAgents].find((n) => n.id === id);

	const { deleteElements } = useSvelteFlow();

	const deleteAgent = () => {
		deleteElements({ nodes: [{ id }] });
		// agents are being updated using nodes automatically so dw about deleting and adding agents in this file
	};

	if (!agent) {
		deleteAgent();
	}
</script>

<Card.Root
	class="group flex aspect-[3/4] w-80 flex-col items-center justify-center overflow-hidden rounded-lg border-none bg-surface text-center shadow-md transition-all duration-300 hover:shadow-xl"
>
	{#if agent}
		<img
			src={agent.avatar}
			alt={`Entry Avatar`}
			class="flex w-full flex-1 items-center justify-center object-cover object-bottom transition-transform duration-500 group-hover:scale-105"
		/>

		<div class="absolute left-0 top-0 flex items-center justify-center p-2 text-center">
			<Badge variant="outline" class="self-center">{agent.model}</Badge>
		</div>

		<div
			class="absolute bottom-0 left-0 right-0 m-1 flex flex-col items-center justify-center gap-1 rounded-md bg-black/60 p-1"
		>
			<h2 class="text-xl">{agent.title}</h2>
			<p class="text-md pb-1">{agent.role}</p>
			<Button href="/app/agents" class="w-full">Edit Agent</Button>
		</div>

		<button
			on:click={() => {
				deleteAgent();
			}}
			aria-label="delete agent"
			type="button"
			class="absolute right-0 top-0 z-10 m-2 rounded-sm bg-background/60 p-1 text-white transition-all duration-300 disabled:pointer-events-none group-hover:scale-125"
		>
			<div class="transition-all duration-100 hover:scale-125">
				<X />
				<span class="sr-only">Delete</span>
			</div>
		</button>
	{/if}
</Card.Root>
