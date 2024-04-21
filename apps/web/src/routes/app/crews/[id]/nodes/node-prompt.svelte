<script lang="ts">
	import type { Writable } from 'svelte/store';
	import { type NodeProps } from '@xyflow/svelte';

	import * as Card from '$lib/components/ui/card';
	import { PromptEditor } from '$lib/components/ui/prompt-editor';

	type $$Props = NodeProps;

	export let data: { prompt: Writable<string> };

	const { prompt } = data;
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Prompt</Card.Title>
	</Card.Header>

	<Card.Content class="grid w-[300px] gap-2">
		<PromptEditor bind:value={$prompt} />
	</Card.Content>
</Card.Root>
