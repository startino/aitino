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
	import { MoreHorizontal } from 'lucide-svelte';

	export let data: PageData;

	const { recentSession, allSessions, recentCrew } = data;

	let loadingSession = true;
	let awaitingReply = false;

	let activeSession = recentSession;
	let messages: Message[] = [];

	onMount(() => {
		loadingSession = false;

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
				loadingSession = false;
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
		loadingSession = true;

		const url = `${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${activeSession.profileId}`;

		main(url);
	}

	async function loadSession(sessionId: string, crewId: string) {
		activeSession.session = null;
		let response = await fetch(`/api/get-messages?sessionId=${sessionId}`);
		messages = await response.json();
		loadingSession = true;

		const url = `${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${activeSession.profileId}&session_id=${sessionId}&reply=""`;

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
		{#if loadingSession}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>Loading...</h1>
			</div>
		{:else if activeSession.session}
			<Chat
				sessionId={activeSession?.session?.id}
				name={activeSession?.session.name}
				{messages}
				{awaitingReply}
				replyCallback={replySession}
			/>
		{:else if recentCrew}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>It looks like you don't have session yet...</h1>
				{#await recentCrew}
					<p>Loading...</p>
				{:then recentCrew}
					<Button on:click={() => startSession(recentCrew.id)}>Run Your Crew!</Button>
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
				crew id: {recentCrew?.id ?? 'missing'} - session id: {activeSession?.session?.id ??
					'missing'}
			</code>
		</div>
	</div>
	<div class="bg-card border-border m-8 w-full max-w-[300px] rounded-md border">
		<div class="flex flex-col items-center justify-center gap-4 p-4">
			<h1 class="text-2xl">Select Session</h1>

			{#if recentCrew}
				<Button class="mb-6 w-full" on:click={() => startSession(recentCrew.id)}
					>Start New Session</Button
				>
			{/if}
			<ul class="flex w-full flex-col gap-2">
				{#await allSessions}
					<p>Loading...</p>
				{:then allSessions}
					{#each allSessions as session}
						<li class="w-full">
							<Button
								variant="outline"
								class="w-full {activeSession.session == session ? 'bg-accent/10' : ''}"
								on:click={() => loadSession(session.id, session.crew_id)}
								>{session.name}
								{#if activeSession.session == session}
									<Button variant="icon"><MoreHorizontal size="16" /></Button>
								{/if}
							</Button>
						</li>
					{/each}
				{/await}
			</ul>
			{activeSession}
			{activeSession.session}
			{activeSession.session?.name}
			{recentCrew}
		</div>
	</div>
</main>
