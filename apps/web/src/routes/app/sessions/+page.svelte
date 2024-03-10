<script lang="ts">
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import Chat from './Chat.svelte';
	import { onMount } from 'svelte';
	import { PUBLIC_API_URL } from '$env/static/public';
	import type { Message, Session } from '$lib/types/models';
	import type { PageData } from './$types';
	import { Loader2 } from 'lucide-svelte';
	import SessionNavigator from './SessionNavigator.svelte';

	export let data: PageData;

	let { recentSession, allSessions, recentCrew, sessionMessages, newSession } = data;

	let activeSession: Session | null = recentSession;
	let messages: Message[] = sessionMessages;

	// Reactivity for the Crew chat
	let statusText = 'Loading everything...';
	let waitingforUser = false;

	onMount(async () => {
		if (newSession.crewId && newSession.title) {
			startNewSession(newSession.crewId, newSession.title);
		}
	});

	async function startNewSession(crewId: string, title: string) {
		// Reset the local variables
		activeSession = null;
		messages = [];

		// Instantiate and get the new session
		const res = await fetch(
			`${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${data.session?.user.id}`
		)
			.then((response) => {
				if (response.status === 200) {
					return response.json();
				} else {
					throw new Error('Failed to start new session');
				}
			})
			.catch((error) => {
				console.error('Failed to start new session', error);
				statusText = 'Failed to start new session';
			});

		const sessionId = res.session_id;

		if (sessionId) {
			statusText = 'Loading your new session...';
			await loadSession(sessionId);
			statusText = 'Session loaded!';
		} else {
			console.error('Failed to start new session');
			statusText = 'Failed to start new session';
		}

		// Set it up locally
		const sessionResponse = await fetch(`?/get-session?sessionId=${sessionId}`);
		const session = await sessionResponse.json();
		activeSession = session;
	}

	async function loadSession(sessionId: string | null = null) {
		console.log('sessionId', sessionId);
		let res = await fetch(`/api/get-session?sessionId=${sessionId}`)
			.then((res) => res.json())
			.then((data) => {
				activeSession = data.session;
			});
		let messageResponse = await fetch(`?/get-messages?sessionId=${sessionId}`);
		messages = await messageResponse.json();
	}

	async function loadMessage(sessionId: string) {
		const res = await fetch(`?/get-session?sessionId=${sessionId}`);
		const data = await res.json();
		const session = data.session;
	}

	function redirectToCrewEditor() {
		window.location.href = '/app/editor/crew';
	}
</script>

<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
		{#if !activeSession}
			{#if recentCrew}
				<div
					class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
				>
					<h1>It looks like you haven't started a session yet...</h1>
					{#await recentCrew}
						<p>Loading...</p>
					{:then recentCrew}
						<Button on:click={() => startNewSession(recentCrew.id, 'New Session')}
							>Run Your Crew!</Button
						>
					{:catch}
						<p>Failed to load crew</p>
					{/await}
				</div>
			{:else}
				<div
					class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto mt-auto flex h-full max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
				>
					<h1>Looks like you haven't created your own crew yet...</h1>
				</div>
			{/if}
		{:else}
			<Chat
				session={activeSession}
				name={activeSession?.title}
				{messages}
				waitingForUser={waitingforUser}
			/>
		{/if}
	</div>
	{#await allSessions}
		<Loader2 />
	{:then allSessions}
		<SessionNavigator
			{allSessions}
			{activeSession}
			{recentCrew}
			on:handleLoadSession={(e) => loadSession(e.detail.id)}
			on:handleStartNewSession={(e) => startNewSession(e.detail.crewId, e.detail.title)}
		/>
	{:catch}
		<p>Failed to load sessions</p>
	{/await}
</div>
