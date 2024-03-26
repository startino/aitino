<script lang="ts">
	import { SendHorizonal, Loader2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';
	import MessageItem from './Message.svelte';
	import * as models from '$lib/types/models';
	import { afterUpdate } from 'svelte';
	import { supabase } from '$lib/supabase';
	import { toast } from 'svelte-sonner';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { ScrollArea } from '$lib/components/ui/scroll-area';

	export let session: models.Session;
	export let messages: models.Message[];
	export let agents: models.Agent[];

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
			async (payload) => {
				console.log(payload);
				const message = payload.new as models.Message;
				console.log(message);
				messages = [...messages, message];
			}
		)
		.subscribe((status) => {
			if (status === 'SUBSCRIBED') {
				console.log('connected to message-insert-channel');
			} else {
				console.error('message-insert-channel status: ' + status);
			}
		});

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
				console.log(payload);
				const session = payload.new as models.Session;
				console.log(session);
				// TODO: Set local status based on message status
			}
		)
		.subscribe((status) => {
			if (status === 'SUBSCRIBED') {
				console.log('connected to session-update-channel');
			} else {
				console.error('session-update-channel status: ' + status);
			}
		});

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
		await fetch(
			`${PUBLIC_API_URL}/crew?id=${session.crew_id}&profile_id=${session.profile_id}&session_id=${session.id}&reply=${newMessageContent}`
		);

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
		class="flex h-full max-h-screen w-full flex-col gap-4 overflow-y-scroll pb-24 pt-14 transition-all duration-500"
		bind:this={chatContainerElement}
	>
		<!-- TODO: add scroll to the bottom of the chat button -->
		{#if messages}
			{#if messages.length > 0}
				{#each messages as message, index}
					{#if index !== 0}
						<MessageItem {message} {agents} />

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
		{:else}
			<div class="flex w-full items-center justify-center gap-4">
				<p>Loading messages...</p>
			</div>
		{/if}

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
