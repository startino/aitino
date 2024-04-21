<script lang="ts">
	import { type NodeProps, useSvelteFlow } from '@xyflow/svelte';
	import { X } from 'lucide-svelte';

	// 👇 always import the styles
	import '@xyflow/svelte/dist/style.css';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { getContext } from '$lib/utils';
	import { toast } from 'svelte-sonner';

	const { crew, agents } = getContext('crew');

	type $$Props = NodeProps;

	export let id: NodeProps['id'];

	let isReceiver = false;

	const agent = $agents.find((n) => n.id === id);

	if (!agent) {
		toast.error(`Error: Agent ${id} not found, please refresh the page.`);
	}

	$: if (isReceiver && agent) {
		$crew.receiver_id = agent.id;
	}

	const { deleteElements } = useSvelteFlow();
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
			<Badge variant="outline" class="self-center"
				>{agent.llm_model_id == 1 ? 'gpt-4-turbo' : 'gpt-3.5-turbo'}</Badge
			>
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
				deleteElements({ nodes: [{ id }] });

				if (isReceiver) {
					$crew.receiver_id = '00000000-0000-0000-0000-000000000000';
				}
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
