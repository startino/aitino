<script lang="ts">
	import Chat from './Chat.svelte';
	import SessionNavigator from './SessionNavigator.svelte';
	import { Loader2 } from 'lucide-svelte';

	export let data;

	let profileId = data.profileId;
	let crew = data.crew;
	let crews = data.crews;
	let session = data.session;
	let sessions = data.sessions;
	let messages = data.messages;
	let agents = data.agents;
</script>

<h1 class="fixed top-4 pl-4 text-2xl font-bold">{session.title} - {crew.title}</h1>
<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
		<Chat {session} {messages} {agents} />
	</div>
	{#if sessions}
		<SessionNavigator {profileId} {sessions} {crews} {session} />
	{:else}
		<Loader2 />
	{/if}
</div>
