<script lang="ts">
	import MessageItem from './Message.svelte';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import { getContext } from '$lib/context';
	import { Separator } from '$lib/components/ui/separator';

	let { messages, agents } = getContext('session');

	$messages.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
</script>

{#each $messages as message, index}
	<MessageItem {message} agents={$agents} />

	{#if index !== $messages.length - 1}
		<Separator class="my-12 scale-95 opacity-50" />
	{/if}
{/each}
