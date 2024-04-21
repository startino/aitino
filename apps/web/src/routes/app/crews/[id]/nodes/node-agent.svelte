<script lang="ts">
	import { type NodeProps, useSvelteFlow, useConnection } from '@xyflow/svelte';
	import { X } from 'lucide-svelte';

	// 👇 always import the styles
	import '@xyflow/svelte/dist/style.css';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { getContext } from '$lib/utils';
	import { Avatar } from '$lib/components/ui/avatar/';
	import Skeleton from '$lib/components/ui/skeleton/skeleton.svelte';
	import { toast } from 'svelte-sonner';
	import type { Writable } from 'svelte/store';

	const { receiver, count, nodes } = getContext('crew');

	type $$Props = NodeProps;

	export let data: {
		avatar: string;
		title: Writable<string>;
		description: Writable<string>;
		model: Writable<string>;
		role: Writable<string>;
	};

	const { avatar, title, description, model, role } = data;

	export let id: NodeProps['id'];

	let isReceiver = false;

	$: if (isReceiver) {
		const me = $nodes.find((n) => n.id === id);
		if (!me) {
			toast.error(`Node didn't find itself somehow`);
		} else {
			$receiver = { node: me, targetCount: 1 };
		}
	}

	const { deleteElements } = useSvelteFlow();
</script>

<Card.Root class="{isReceiver ? 'bg-primary-950' : ''} aspect-1 w-[300px] transition-all">
	<button
		on:click={() => {
			deleteElements({ nodes: [{ id }] });
			$count.agents--;

			if (isReceiver) {
				$receiver = null;
			}
		}}
		aria-label="delete agent"
		type="button"
		class="absolute right-2 top-2 z-10 rounded-sm bg-background/60 p-1 text-white transition-all duration-300 disabled:pointer-events-none group-hover:scale-125"
	>
		<div class="transition-all duration-100 hover:scale-125">
			<X />
			<span class="sr-only">Delete</span>
		</div>
	</button>

	<Card.Header class="flex gap-2 text-center">
		<Card.Title class="mt-4">
			<p>
				{title}
				{#if isReceiver}
					(Receiver)
				{/if}
			</p>
			<label for="is-receiver">Receiver</label>
			<input id="is-receiver" name="is-receiver" bind:value={isReceiver} type="checkbox" />
		</Card.Title>
		<Card.Description>{role}</Card.Description>
		{#if avatar}
			<Avatar class="mx-auto h-24 w-24">
				<Skeleton class="h-24 w-24 rounded-full" />
				<img src={avatar} alt="" />
			</Avatar>
		{/if}
		<Badge variant="outline" class="self-center">{model}</Badge>
	</Card.Header>
	<Card.Content class="grid gap-2 text-center">
		<p class="line-clamp-3 text-ellipsis">{description}</p>
		<Button href="/app/agents">Edit Agent</Button>
		<!-- <Handle type="target" id="top-{id}" position={Position.Top} /> -->
		<!-- <Handle type="source" id="bottom-{id}" position={Position.Bottom} /> -->
	</Card.Content>
</Card.Root>
