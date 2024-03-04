<script lang="ts">
	import type { SessionLoad } from '$lib/types/loads';
	import { Button } from '$lib/components/ui/button';
	import Chat from './Chat.svelte';
	import { onMount } from 'svelte';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { error } from '@sveltejs/kit';
	import type { Message, Session } from '$lib/types/models';
	import { get, writable } from 'svelte/store';
	import type { PageData } from './$types';

	export let data: PageData;

	const { recentSession, allSessions } = data;

	let loading = true;
	let awaitingReply = false;

	let activeSession = recentSession;
	let messages: Message[] = [];

	onMount(() => {
		loading = false;

		if (messages.length > 0) {
			awaitingReply = true;
		}
	});

	async function* callCrew(url: string): AsyncGenerator<string, void, unknown> {
		const response = await fetch(url);
		const reader = response.body?.getReader();

		if (!reader) {
			throw new Error('Invalid response');
		}

		while (true) {
			const { done, value } = await reader.read();

			if (done) {
				break;
			}

			const line = new TextDecoder().decode(value);

			if (!line) {
				break;
			}

			yield line;
		}
	}

	async function main(url: string): Promise<void> {
		if (!url) {
			console.log('Usage: Provide a valid URL as a parameter');
			return;
		}

		for await (const event of callCrew(url)) {
			let e = null;
			try {
				e = JSON.parse(event.trim());
				console.log('got message', e);
			} catch (error) {
				console.error(`Error parsing JSON ${error}:`, event);
				continue;
			}
			if (!e) {
				continue;
			}

			if (e.id === 0) {
				activeSession.session = {
					id: e.data.session_id,
					crew_id: e.data.maeva_id,
					profile_id: e.data.profile_id,
					created_at: e.data.created_at
				};
				loading = false;
				console.log('got session id', e.data.session_id);
				continue;
			}
			if (e.data === 'done') {
				awaitingReply = true;
				console.log('done');

				return;
			}

			messages = [...messages, e.data];
		}
	}

	function startSession(crewId: string) {
		activeSession.session = null;
		messages = [];
		loading = true;

		const url = `${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${activeSession.profileId}`;

		main(url);
	}

	function replySession(message: string) {
		if (!activeSession.session) {
			throw error(500, 'Cannot reply without session');
		}
		awaitingReply = false;
		const url = `${PUBLIC_API_URL}/crew?id=${activeSession.crewId}&profile_id=${activeSession.profileId}&session_id=${activeSession.session.id}&reply=${message}`;

		main(url);
	}

	function redirectToCrewEditor() {
		window.location.href = '/app/editor/crew';
	}
</script>

<main class="flex h-full flex-row">
	<div class="w-full">
		{#if loading}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>Loading...</h1>
			</div>
		{:else if activeSession.session}
			<Chat
				sessionId={activeSession?.session?.id}
				{messages}
				{awaitingReply}
				replyCallback={replySession}
			/>
		{:else if data.recentCrew}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>It looks like you don't have session yet...</h1>
				{#await data.recentCrew}
					<p>Loading...</p>
				{:then recentCrew}
					<Button on:click={() => startSession(data.recentCrew?.id)}>Run Your Crew!</Button>
				{:catch}
					<p>Failed to load crew</p>
				{/await}
			</div>
		{:else}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>It looks like you haven't created a crew yet...</h1>
				<Button on:click={redirectToCrewEditor}>Go Create One!</Button>
			</div>
		{/if}
		<div class="absolute bottom-1 mx-auto flex h-min w-full flex-col items-center justify-center">
			<code class="text-muted">debug:</code>
			<code class="text-muted">
				crew id: {activeSession?.crewId ?? 'missing'} - session id: {activeSession?.session?.id ??
					'missing'}
			</code>
		</div>
	</div>
	<div class="bg-card border-border m-8 w-full max-w-[300px] rounded-md border">
		<div class="flex flex-col items-center justify-center gap-4 p-4">
			<h1 class="text-2xl">Select Session</h1>

			{#if data.recentCrew}
				<Button on:click={() => startSession(data.recentCrew.id)}>Start New Session</Button>
			{/if}
			<ul>
				{#await allSessions}
					<p>Loading...</p>
				{:then allSessions}
					{#each allSessions as session}
						<li>
							<Button on:click={() => startSession(session.crew_id)}>{session.id}</Button>
						</li>
					{/each}
				{/await}
			</ul>
		</div>
	</div>
</main>
