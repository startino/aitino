<script lang="ts">
	import { type NodeProps } from '@xyflow/svelte';

	import * as Card from '$lib/components/ui/card';
	import { PromptEditor } from '$lib/components/ui/prompt-editor';
	import { getContext } from '$lib/utils';
	let { crew } = getContext('crew');

	let prompt = $crew.prompt ? $crew.prompt.content : '';
	$: $crew.prompt = {
		id: '00000000-0000-0000-0000-000000000000',
		title: 'prompt',
		content: prompt
	};

	type $$Props = NodeProps;

	export const data = {};
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Prompt</Card.Title>
	</Card.Header>

	<Card.Content class="grid w-[300px] gap-2">
		<PromptEditor bind:value={prompt} />
	</Card.Content>
</Card.Root>
