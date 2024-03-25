<script lang="ts">
	import type { Writable } from 'svelte/store';
	import { Position, useHandleConnections, useSvelteFlow, type NodeProps } from '@xyflow/svelte';
	import { X } from 'lucide-svelte';

	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import Handle from '$lib/components/Handle.svelte';
	import { getContext } from '$lib/utils';
	import { PromptEditor } from '$lib/components/ui/prompt-editor';

	type $$Props = NodeProps;

	export let data: { title: Writable<string>; content: Writable<string> };
	export let id: $$Props['id'];

	const { content, title } = data;

	const { receiver, count } = getContext('crew');
	const connects = useHandleConnections({ nodeId: id, type: 'source' });
	const { deleteElements } = useSvelteFlow();

	$: isConnectable = $connects.length === 0;
</script>

<Card.Root>
	<button
		on:click={() => {
			deleteElements({ nodes: [{ id }] });
			$count.prompts--;

			if ($receiver) {
				$receiver.targetCount--;
				$receiver.targetCount === 0 && ($receiver = null);
			}
		}}
		aria-label="delete agent"
		class="absolute right-2 top-2"><X /></button
	>
	<Card.Header>
		<Card.Title>Prompt</Card.Title>
	</Card.Header>

	<Card.Content class="grid w-[300px] gap-2">
		<Input bind:value={$title} placeholder="Title..." />
		<PromptEditor bind:value={$content} />
		<Handle
			type="source"
			id="bottom-{id}"
			position={Position.Bottom}
			onconnect={(c) => {
				if (c.length >= 1) {
					isConnectable = false;
				}
			}}
			ondisconnect={(c) => {
				isConnectable = true;
			}}
			{isConnectable}
		/>
	</Card.Content>
</Card.Root>
