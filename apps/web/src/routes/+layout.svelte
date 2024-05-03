<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import '$styling';
	import { onMount } from 'svelte';
	import { Toaster } from 'svelte-sonner';
	import { supabase } from '$lib/supabase/client';

	export let data;

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

{#if data.user}
	<p class="fixed top-10">yes</p>
{:else}
	<p class="fixed top-10">no</p>
{/if}

<slot />
