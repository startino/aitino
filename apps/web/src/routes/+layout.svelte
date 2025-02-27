<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import '$styling';
	import { Toaster } from 'svelte-sonner';
</script>

<Toaster />

<slot />
