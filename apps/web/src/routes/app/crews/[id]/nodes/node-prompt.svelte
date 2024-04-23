<script lang="ts">
	import { type NodeProps } from '@xyflow/svelte';

	import * as Card from '$lib/components/ui/card';
	import { PromptEditor } from '$lib/components/ui/prompt-editor';
	import { getContext } from '$lib/utils';
	let { crew } = getContext('crew');

	type $$Props = NodeProps;

	export const data = {};
</script>

<Card.Root>
	<Card.Header>
		<Card.Title>Prompt</Card.Title>
	</Card.Header>

	<Card.Content class="grid w-[300px] gap-2">
		<PromptEditor bind:value={$crew.prompt} />
	</Card.Content>
</Card.Root>
