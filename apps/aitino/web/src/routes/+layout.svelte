<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import '$styling';
	import { onMount } from 'svelte';
	import { Toaster } from 'svelte-sonner';
	import { supabase } from '$lib/supabase/client';

	onMount(() => {
		const { data } = supabase.auth.onAuthStateChange(() => {
			invalidateAll();
		});

		return () => {
			data.subscription.unsubscribe();
		};
	});
</script>

<Toaster />

<slot />
