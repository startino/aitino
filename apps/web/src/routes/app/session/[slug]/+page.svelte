<script lang="ts">
	import type { SessionLoad } from '$lib/types/loads';
	import Chat from './Chat.svelte';
	import SessionNavigator from './SessionNavigator.svelte';
	import { Loader2 } from 'lucide-svelte';
	import * as models from '$lib/types/models';

	export let data: SessionLoad;

	let profileId: string = data.profileId;
	let crew: models.Crew = data.crew;
	let crews: models.Crew[] = data.crews;
	let session: models.Session = data.session;
	let sessions: models.Session[] = data.sessions;
	let messages: models.Message[] = data.messages;
	let agents: models.Agent[] = data.agents;
</script>

<h1 class="fixed top-4 pl-4 text-2xl font-bold">{session.title}</h1>
<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
		<Chat {session} {messages} {agents} />
	</div>
	{#if sessions}
		<SessionNavigator {profileId} {sessions} {crew} {session} />
	{:else}
		<Loader2 />
	{/if}
</div>
