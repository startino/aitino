<script lang="ts">
	import { Position, type NodeProps, useSvelteFlow, useConnection } from '@xyflow/svelte';
	import { X } from 'lucide-svelte';

	// 👇 always import the styles
	import '@xyflow/svelte/dist/style.css';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import Handle from '$lib/components/Handle.svelte';
	import { getContext } from '$lib/utils';
	import { Avatar } from '../avatar/';
	import Skeleton from '../skeleton/skeleton.svelte';

	type $$Props = NodeProps;

	const { receiver, count } = getContext('crew');

	export let data: {
		avatar: string;
		title: string;
		description: string;
		model: string;
		role: string;
	};

	export let id: NodeProps['id'];

	const connection = useConnection();

	let isConnecting = false;
	let isTarget = false;

	$: isConnecting = !!$connection.startHandle?.nodeId;
	$: isTarget = !!$connection.startHandle && $connection.startHandle?.nodeId !== id;
	$: isReceiver = $receiver?.node.id === id;

	const { deleteElements } = useSvelteFlow();
</script>

<Card.Root
	class="{isTarget ? 'border-2 border-dashed bg-card ' : ''} {isReceiver
		? 'bg-primary-950'
		: ''} aspect-1transition w-[300px]"
>
	<button
		on:click={() => {
			deleteElements({ nodes: [{ id }] });
			$count.agents--;

			if (isReceiver) {
				$receiver = null;
			}
		}}
		aria-label="delete agent"
		class="absolute right-2 top-2"><X /></button
	>

	<Card.Header class="flex gap-2 text-center">
		<Card.Title class="mt-4">
			<p>
				{data.title}
				{#if isReceiver}
					(Receiver)
				{/if}
			</p>
		</Card.Title>
		<Card.Description>{data.role}</Card.Description>
		{#if data.avatar}
			<Avatar class="mx-auto h-24 w-24">
				<Skeleton class="h-24 w-24 rounded-full" />
				<img src={data.avatar} alt="" />
			</Avatar>
		{/if}
		<Badge variant="outline" class="self-center">{data.model}</Badge>
	</Card.Header>
	<Card.Content class="grid gap-2 text-center">
		<p class="line-clamp-3 text-ellipsis">{data.description}</p>
		<Button href="/app/agents/editor">Edit Agent</Button>
		<Handle type="target" id="top-{id}" position={Position.Top} />
		<Handle type="source" id="bottom-{id}" position={Position.Bottom} />
	</Card.Content>
</Card.Root>
