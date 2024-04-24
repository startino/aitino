<script lang="ts">
	import { getContext, setContext } from '$lib/utils';
	import { writable } from 'svelte/store';
	import Chat from './Chat.svelte';
	import SessionNavigator from './SessionNavigator.svelte';
	import type { SessionContext } from '$lib/types';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Button } from '$lib/components/ui/button/index.js';

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

<h1 class="fixed left-[13em] right-0 top-0 z-10 w-full bg-background p-2 text-2xl font-bold">
	{$session.title} - {$crew.title}
</h1>
<div class="flex flex-col px-12 pt-12">
	<Chat />
	<div class="my-8 flex h-full w-full items-center justify-center gap-2">
		<Textarea bind:value={$session.reply}></Textarea>
		<Button>Send</Button>
	</div>
</div>
<SessionNavigator />
