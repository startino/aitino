<script lang="ts">
	import { SendHorizonal, Loader2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import MessageItem from './Message.svelte';
	import type { Message, Session } from '$lib/types/models';
	import { afterUpdate } from 'svelte';
	import { supabase } from '$lib/supabase';
	import { toast } from 'svelte-sonner';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	export let session: Session;
	export let name: string;
	export let messages: Message[];

	// Reactivity
	export let waitingForUser = true;

	let rows = 1;
	$: minRows = rows <= 1 ? 1 : rows >= 50 ? 50 : rows;

	supabase
		.channel('message-insert-channel')
		.on(
			'postgres_changes',
			{
				event: 'INSERT',
				schema: 'public',
				table: 'messages',
				filter: `session_id=eq.${session.id}`
			},
			async (payload) => (messages = [...messages, payload.new as Message])
		)
		.subscribe((status) => messagesSubscribed(status));

	supabase
		.channel('session-update-channel')
		.on(
			'postgres_changes',
			{
				event: 'UPDATE',
				schema: 'public',
				table: 'sessions',
				filter: `id=eq.${session.id}`
			},
			async (payload) => {
				// TODO: Set local status based on message status
			}
		)
		.subscribe((status) => sessionSubscribed(status));

	function sessionSubscribed(status: string) {
		if (status === 'SUBSCRIBED') {
			//console.log('connected to session channel');
		} else {
			//console.log(status);
		}
	}

	function setLocalStatus(status: string) {
		if (status === 'awaiting_user') {
			waitingForUser = true;
		} else {
			waitingForUser = false;
		}
	}

	function messagesSubscribed(status: string) {
		if (status === 'SUBSCRIBED') {
			//console.log('connected to message channel');
		} else {
			//console.log(status);
		}
	}

	async function loadNewMessage(message: Message) {
		messages = [...messages, message];
	}

	function handleInputChange(event: { target: { value: string } }) {
		newMessageContent = event.target.value;
		rows = newMessageContent.split('\n').length;
	}

	let newMessageContent = '';
	async function sendMessage() {
		if (newMessageContent.trim().length <= 5) {
			console.warn('Message too short');
			toast.error('Message too short');
		}

		// 'Resume' the conversation to Crew API
		const url = `${PUBLIC_API_URL}/crew?id=${session.crew_id}&profile_id=${session.profile_id}&session_id=${session.id}&reply=${newMessageContent}`;
		const apiRes = await fetch(url);
		const apiData = await apiRes.json();
		console.log(apiData);

		// Update the session status on the DB
		const res = await fetch(`?/set-status?session.id=${session.id}?status=awaiting_agent`);
		const data = await res.json();

		// Update local status
		waitingForUser = true;

		//messages = [...messages, newMessageContent];
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
	<ScrollArea
		class="flex h-full max-h-screen w-full flex-col gap-4 overflow-y-scroll pb-24 pt-20 transition-all duration-500"
		bind:this={chatContainerElement}
	>
		<h1 class="mb-6 text-center text-3xl font-bold">{name}</h1>
		<!-- TODO: add scroll to the bottom of the chat button -->
		{#await messages}
			<div class="flex w-full items-center justify-center gap-4">
				<p>Loading messages...</p>
			</div>
		{:then messages}
			{#if messages.length > 0}
				{#each messages as message, index}
					{#if message.content != 'CONTINUE'}
						<MessageItem {message} />

						{#if index !== messages.length - 1}
							<hr class="prose my-20 w-full max-w-none border-t border-nsecondary px-12" />
						{/if}
					{/if}
				{/each}
			{:else}
				<div class="flex w-full items-center justify-center gap-4">
					<p>No messages have been sent yet.</p>
				</div>
			{/if}
		{/await}

		<div
			class="absolute bottom-4 left-1/2 flex w-full max-w-4xl -translate-x-1/2 flex-row items-center justify-center gap-1 bg-surface"
		>
			<div
				class="mx-auto flex w-full max-w-4xl flex-row rounded-md border border-border bg-card {waitingForUser
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
					class="prose prose-main w-full max-w-none resize-none rounded-l border-none bg-card text-lg"
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
					class="hover:bg-default flex place-items-center hover:scale-95 hover:text-primary"
					disabled={newMessageContent.length <= 5 || !waitingForUser}
					on:click={sendMessage}
				>
					<SendHorizonal size="24" class="mx-auto my-auto" />
				</Button>
			</div>
		</div>
	</ScrollArea>
</main>
