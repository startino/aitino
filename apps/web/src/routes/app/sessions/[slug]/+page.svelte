<script lang="ts">
	import { getContext, setContext } from '$lib/utils';
	import { writable } from 'svelte/store';
	import Chat from './Chat.svelte';
	import SessionNavigator from './SessionNavigator.svelte';
	import { Loader2 } from 'lucide-svelte';
	import type { SessionContext } from '$lib/types';

	export let data;

	let writableData: SessionContext = {
		profileId: writable(data.profileId),
		session: writable(data.session),
		sessions: writable(data.sessions),
		crew: writable(data.crew),
		crews: writable(data.crews),
		messages: writable(data.messages),
		agents: writable(data.agents)
	};

	setContext('session', writableData);
	let { session, sessions, crew } = getContext('session');
</script>

<h1 class="fixed top-4 pl-4 text-2xl font-bold">{$session.title} - {$crew.title}</h1>
<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
		<Chat />
	</div>
	{#if sessions}
		<SessionNavigator />
	{:else}
		<Loader2 />
	{/if}
</div>
