<script lang="ts">
	import { Send, SendHorizonal, Shell, Loader2, Loader } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import MessageItem from './Message.svelte';
	import type { Message } from '$lib/types/models';
	import { afterUpdate } from 'svelte';
	import { supabase } from '$lib/supabase';
	import SuperDebug from 'sveltekit-superforms/client/SuperDebug.svelte';
	export let sessionId: string;
	export let name: string;
	export let messages: Message[];

	// Reactivity
	export let waitingForUser = true;

	export let replyCallback: (message: string) => void;

	let rows = 1;
	$: minRows = rows <= 1 ? 1 : rows >= 50 ? 50 : rows;

	const channel = supabase
		.channel('message-insert-channel')
		.on(
			'postgres_changes',
			{
				event: 'INSERT',
				schema: 'public',
				table: 'messages',
				filter: `session_id=eq.${sessionId}`
			},
			(payload) => loadNewMessage(payload.new as Message)
		)
		.subscribe((status) => sessionSubscribed(status));

	function sessionSubscribed(status: string) {
		if (status === 'SUBSCRIBED') {
			console.log('connected');
		} else {
			console.log(status);
		}
	}

	async function loadNewMessage(message: Message) {
		messages = [...messages, message];
		console.log('new message: ', messages);
		chatContainerElement.scrollTop = chatContainerElement.scrollHeight + 500;
		// // Check if its the user's turn to speak
		// const response = await fetch(`http:/localhost:5173/api/get-session?sessionId=${sessionId}`);
		// const session = await response.json();
		// if (session.status === 'awaiting_user') {
		// 	waitingForUser = true;
		// } else {
		// 	waitingForUser = false;
		// }
	}

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
		class="flex max-h-screen w-full flex-col gap-4 overflow-y-scroll pb-24 pt-20 transition-all duration-500"
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
				{#if message.content != 'CONTINUE'}
					<MessageItem {message} />

					{#if index !== messages.length - 1}
						<hr class="prose border-nsecondary my-20 w-full max-w-none border-t px-12" />
					{/if}
				{/if}
			{/each}
		{/await}

		<div
			class="bg-surface absolute bottom-4 left-1/2 flex w-full max-w-5xl -translate-x-1/2 flex-row items-center justify-center gap-1"
		>
			<div
				class="bg-card border-border mx-auto flex w-full max-w-4xl flex-row rounded-md border {waitingForUser
					? ''
					: 'cursor-not-allowed'}"
			>
				<div class="flex place-items-center rounded-md">
					<Loader2
						size="24"
						class="ml-2 animate-spin rounded-full {waitingForUser ? 'hidden' : ' text-amber-500'}"
					/>
				</div>
				<Textarea
					class="prose prose-main bg-card w-full max-w-none resize-none rounded-l border-none text-lg"
					placeholder={waitingForUser
						? 'Give Feedback to the agents'
						: 'Waiting for the crew to finish...'}
					bind:value={newMessageContent}
					disabled={!waitingForUser}
					{minRows}
					maxRows={minRows}
					on:input={handleInputChange}
				></Textarea>
				<Button
					variant="ghost"
					class="hover:bg-default hover:text-primary flex place-items-center hover:scale-95"
					disabled={newMessageContent.length <= 5 || !waitingForUser}
					on:click={sendMessage}
				>
					<SendHorizonal size="24" class="mx-auto my-auto" />
				</Button>
			</div>
		</div>
	</div>
</main>
