<script lang="ts">
	import MessageItem from './Message.svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { getContext } from '$lib/utils';
	import { Separator } from '$lib/components/ui/separator';

	let { messages, agents } = getContext('session');
</script>

{#each $messages as message, index}
	{#if index !== 0}
		<MessageItem {message} agents={$agents} />

		{#if index !== $messages.length - 1}
			<Separator class="my-12 scale-95 opacity-50" />
		{/if}
	{/if}
{/each}
