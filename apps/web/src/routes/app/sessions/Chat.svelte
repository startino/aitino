<script lang="ts">
	import { Send, SendHorizonal, Shell, Loader2 } from 'lucide-svelte';
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

<main class="container relative flex max-w-5xl flex-col justify-end overflow-y-hidden">
	<div
		class="flex max-h-screen w-full flex-col gap-4 overflow-y-scroll pb-24 pt-20"
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
			{#if !awaitingReply}
				<div class="flex w-full gap-4 text-lg">
					<p>Waiting for the crew to reply...</p>
					<Loader2 class="animate-spin" size="24" />
				</div>
			{/if}
		{/await}

		<div
			class="bg-surface absolute bottom-4 left-1/2 flex w-full max-w-5xl -translate-x-1/2 flex-row items-center justify-center gap-1"
		>
			<div
				class="bg-card border-border mx-auto flex w-full max-w-4xl flex-row rounded-md border {awaitingReply
					? ''
					: 'cursor-not-allowed'}"
			>
				<div class="flex place-items-center rounded-md">
					<div
						class="m-4 h-3 w-3 animate-ping rounded-full {awaitingReply
							? 'bg-emerald-500'
							: ' bg-amber-500'}"
					></div>
				</div>
				<Textarea
					class="prose prose-main bg-card w-full max-w-none resize-none rounded-l border-none text-lg"
					placeholder={awaitingReply
						? 'Give Feedback to the agents'
						: 'Shh... the crew is working!'}
					bind:value={newMessageContent}
					disabled={!awaitingReply}
					{minRows}
					maxRows={minRows}
					on:input={handleInputChange}
				></Textarea>
				<Button
					variant="ghost"
					class="hover:bg-default hover:text-primary flex place-items-center hover:scale-95"
					disabled={newMessageContent.length <= 5 || !awaitingReply}
					on:click={sendMessage}
				>
					<SendHorizonal size="24" class="mx-auto my-auto" />
				</Button>
			</div>
		</div>
	</div>
</main>
