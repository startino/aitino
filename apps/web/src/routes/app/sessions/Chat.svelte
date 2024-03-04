<script lang="ts">
	import { Send } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import MessageItem from './Message.svelte';
	import type { Message as MessageType } from '$lib/types/models';
	import { afterUpdate } from 'svelte';

	export let sessionId: string;
	export let name: string;
	export let messages: MessageType[] | Promise<MessageType[]>;

	export let awaitingReply = false;

	export let replyCallback: (message: string) => void;

	let rows = 1;
	$: minRows = rows <= 1 ? 1 : rows >= 50 ? 50 : rows;

	function handleInputChange(event: { target: { value: string } }) {
		newMessageContent = event.target.value;
		rows = newMessageContent.split('\n').length;
	}

	let newMessageContent = '';
	function sendMessage() {
		if (newMessageContent.trim().length <= 5) {
			console.warn('Message too short');
			// TODO: show sonner warning to user
		}

		replyCallback(newMessageContent);

		const newMessage = {
			id: crypto.randomUUID(),
			session_id: sessionId,
			recipient: '',
			content: newMessageContent,
			role: 'user',
			name: 'Admin',
			created_at: new Date().toISOString().replace('T', ' ')
		};
		messages = [...messages, newMessage];
		newMessageContent = '';
	}

	let chatContainerElement: HTMLDivElement;
	afterUpdate(() => {
		if (chatContainerElement) {
			chatContainerElement.scrollTop = chatContainerElement.scrollHeight;
		}
	});
</script>

<div class="container flex max-w-6xl flex-col justify-end overflow-y-hidden">
	<div
		class="flex max-h-screen w-full flex-col gap-4 overflow-y-scroll pb-16 pt-20"
		bind:this={chatContainerElement}
	>
		<h1 class="text-center text-3xl font-bold">{name}</h1>
		<!-- TODO: add scroll to the bottom of the chat button -->
		{#await messages}
			<div class="flex w-full items-center justify-center gap-4">
				<p>Loading messages...</p>
			</div>
		{:then messages}
			{#each messages as message, index}
				<MessageItem {message} />

				{#if index !== messages.length - 1}
					<hr class="prose border-nsecondary my-20 w-full max-w-none border-t px-12" />
				{/if}
			{/each}
		{/await}

		{#if awaitingReply}
			<div class="flex w-full flex-row items-center justify-center gap-1 p-1">
				<Textarea
					class="prose prose-main w-full max-w-none resize-none text-lg"
					placeholder="Give Feedback to the agents"
					bind:value={newMessageContent}
					{minRows}
					maxRows={minRows}
					on:input={handleInputChange}
				></Textarea>
				<Button
					variant="ghost"
					class="hover:bg-default hover:text-primary hover:scale-95"
					disabled={newMessageContent.length <= 5}
					on:click={sendMessage}
				>
					<Send />
				</Button>
			</div>
		{/if}
	</div>
</div>
