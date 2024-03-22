<script lang="ts">
	import { Button } from '$lib/components/ui/button';
    import type { SessionsLoad } from '$lib/types/loads';
	import Chat from './Chat.svelte';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { Loader2 } from 'lucide-svelte';
	import SessionNavigator from './SessionNavigator.svelte';
    import * as models from '$lib/types/models';

	export let data: SessionsLoad;

    let crew: models.Crew = data.crew;
    let session: models.Session | null = data.session;
    let sessions: models.Session[] = data.sessions;
    let messages: models.Message[] = data.messages;

	// Reactivity for the Crew chat
	let waitingforUser = false;

	async function startNewSession(crewId: string, title: string) {
		// Reset the local variables
		messages = [];

		// Instantiate and get the new session
		const res = await fetch(
			`${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${data.profileId}`
		)
			.then((response) => {
				if (response.status === 200) {
					return response.json();
				} else {
					throw new Error('Failed to start new session. bad respose: ' + response);
				}
			})
			.catch((error) => {
				console.error('Failed to start new session. error', error);
			});

		const session: models.Session = res.data.session;
        console.log('session: ', session);

		if (!session) {
			console.error('Failed to start new session: ' + JSON.stringify(res));
		}
	}
</script>

<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
		{#if !session}
			{#if crew}
				<div
					class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
				>
					<h1>It looks like you haven't started a session yet...</h1>
					{#if crew}
						<Button on:click={() => startNewSession(crew.id, 'New Session')}
							>Run Your Crew!</Button
						>
					{:else}
						<p>Loading...</p>
					{/if}
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
				session={session}
				name={session?.title}
				messages={messages}
				waitingForUser={waitingforUser}
			/>
		{/if}
	</div>
	{#if sessions}
		<SessionNavigator
			{sessions}
			{crew}
			activeSession={session}
			on:handleLoadSession={(e) => e.detail.session}
			on:handleStartNewSession={(e) => startNewSession(e.detail.crewId, e.detail.title)}
		/>
	{:else}
		<Loader2 />
		<p>Failed to load sessions</p>
	{/if}
</div>
