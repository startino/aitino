<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import '$styling';
	import { onMount } from 'svelte';
	import { Toaster } from 'svelte-sonner';
	import { supabase } from '$lib/supabase/client';
	import { setContext, type RootContext } from '$lib/context';
	import { writable } from 'svelte/store';

	export let data;

	let writableData: RootContext = {
		user: writable(data.user),
		agents: writable(data.agents),
		crews: writable(data.crews),
		sessions: writable(data.sessions),
		apiKeys: writable(data.apiKeys),
        forms: writable(data.forms),
	};

	setContext('root', writableData);

	onMount(() => {
		const { data: d } = supabase.auth.onAuthStateChange(() => {
			invalidateAll();
		});

		return () => {
			d.subscription.unsubscribe();
		};
	});
</script>

<Toaster />

<slot />
