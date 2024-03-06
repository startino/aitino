<script lang="ts">
	import { Position, type NodeProps, useSvelteFlow, useConnection } from '@xyflow/svelte';
	import { type Writable } from 'svelte/store';
	import { X } from 'lucide-svelte';

	// 👇 always import the styles
	import '@xyflow/svelte/dist/style.css';
	import * as Card from '$lib/components/ui/card';
	import * as Select from '$lib/components/ui/select';
	import { Input } from '$lib/components/ui/input';
	import Handle from '$lib/components/Handle.svelte';
	import { getContext } from '$lib/utils';
	import { PromptEditor } from '$lib/components/ui/prompt-editor';
	import { Avatar } from '../avatar/';
	import Skeleton from '../skeleton/skeleton.svelte';

	type $$Props = NodeProps;

	const { receiver, count } = getContext('crew');

	export let data: {
		avatar: string;
		prompt: Writable<string>;
		job_title: Writable<string>;
		name: Writable<string>;
		model: Writable<{ label: string; value: string }>;
	};

	const { name, model, prompt, job_title, avatar } = data;

	const models = [
		{
			label: 'GPT-4 Turbo',
			value: 'gpt-4-turbo-preview'
		},
		{
			label: 'GPT-3.5 Turbo',
			value: 'gpt-3.5-turbo'
		}
	];

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
	class="{isTarget ? 'bg-card border-2 border-dashed ' : ''} {isReceiver
		? 'bg-primary-950'
		: ''} aspect-1transition"
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

	<Card.Header class="flex gap-2">
		<Card.Title class="mt-4">
			{#if isReceiver}
				(Receiver)
			{/if}
			<Input placeholder="Name..." class="text-center" bind:value={$name} />
		</Card.Title>
		{#if avatar}
			<Avatar class="mx-auto h-24 w-24">
				<Skeleton class="h-24 w-24 rounded-full" />
				<img src={avatar} alt="" class="scale-125" />
			</Avatar>
		{:else}{/if}
	</Card.Header>
	<Card.Content class="grid w-[300px] gap-2">
		<Input placeholder="Job title..." bind:value={$job_title} />
		<Select.Root bind:selected={$model}>
			<Select.Trigger>
				<Select.Value placeholder="Select a model" />
			</Select.Trigger>
			<Select.Content>
				<Select.Group>
					{#each models as { value, label }}
						<Select.Item {value} {label}>
							{label}
						</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
		</Select.Root>
		<PromptEditor bind:value={$prompt} />
		<Handle type="target" id="top-{id}" position={Position.Top} />
		<Handle type="source" id="bottom-{id}" position={Position.Bottom} />
	</Card.Content>
</Card.Root>
