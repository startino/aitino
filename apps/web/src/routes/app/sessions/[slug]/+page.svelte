<script lang="ts">
	import { getContext, setContext } from '$lib/utils';
	import { writable } from 'svelte/store';
	import Chat from './Chat.svelte';
	import SessionNavigator from './SessionNavigator.svelte';
	import type { SessionContext } from '$lib/types';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Button } from '$lib/components/ui/button/index.js';
	import { createClient } from '@supabase/supabase-js';
	import { PUBLIC_SUPABASE_ANON_KEY, PUBLIC_SUPABASE_URL } from '$env/static/public';
	import api from '$lib/api';
	import { toast } from 'svelte-sonner';
	import { onMount } from 'svelte';

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
	let { session, messages, crew } = getContext('session');

	const continueSession = async () => {
		if ($session.reply !== '') {
			const reply = `
                Continue the conversation from last time, here is the conversation:
                ${JSON.stringify($messages)}

                The Admin has Replied:
                ${$session.reply}
            `;
			const newSession = await api
				.POST('/sessions/run', {
					body: {
						crew_id: $session.crew_id,
						profile_id: $session.profile_id,
						session_title: $session.title,
						session_id: $session.id,
						reply: reply
					}
				})
				.then(({ data: d, error: e }) => {
					if (e) {
						toast(`Error continueing session: ${e.detail}`);
						return null;
					}
					if (!d) {
						toast(`Error continueing session. No session was returned.`);
						return null;
					}
					return d;
				});

			if (!newSession) return;

			$session = newSession;
			$session.reply = '';
		}
	};

	// Initialize the TS client
	const supabase = createClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY);

	// Create a function to handle inserts
	const handleInserts = (payload: any) => {
		if (payload.new.session_id === $session.id) {
			$messages = [...$messages, payload.new];
			console.log('New message:', payload.new);
			window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
		}
	};

	// Listen to inserts
	supabase
		.channel('messages')
		.on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, handleInserts)
		.subscribe();
</script>

<h1 class="fixed left-[13em] right-0 top-0 z-10 w-full bg-background p-2 text-2xl font-bold">
	{$session.title} - {$crew.title}
</h1>
<div class="flex flex-col px-12 pt-12">
	<Chat />
	<div class="my-8 flex h-full w-full items-center justify-center gap-2">
		<Textarea bind:value={$session.reply}></Textarea>
		<Button on:click={continueSession}>Send</Button>
	</div>
</div>
<SessionNavigator />
