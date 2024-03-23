<script lang="ts">
	import type { SessionLoad } from '$lib/types/loads';
	import Chat from './Chat.svelte';
	import SessionNavigator from './SessionNavigator.svelte';
	import { Loader2 } from 'lucide-svelte';
	import { setContext } from 'svelte';

	export let data: SessionLoad;

	$: crew = data.crew;
	$: crews = data.crews;
	$: session = data.session;
	$: sessions = data.sessions;
	$: messages = data.messages;
	$: agents = data.agents;

	setContext('crew', crew);
	setContext('crews', crews);
	setContext('session', session);
	setContext('sessions', sessions);
	setContext('messages', messages);
	setContext('agents', agents);
</script>

<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
		<Chat />
	</div>
	{#if sessions}
		<SessionNavigator {sessions} {crew} {session} />
	{:else}
		<Loader2 />
	{/if}
</div>
