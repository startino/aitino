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
	let session: models.Session = data.session;
	let sessions: models.Session[] = data.sessions;
	let messages: models.Message[] = data.messages;

	// Reactivity for the Crew chat
	let waitingforUser = false;
</script>

<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
        <Chat {session} name={session?.title} {messages} waitingForUser={waitingforUser} />
	</div>
	{#if sessions}
		<SessionNavigator
			{sessions}
			{crew}
			{session}
		/>
	{:else}
		<Loader2 />
	{/if}
</div>
