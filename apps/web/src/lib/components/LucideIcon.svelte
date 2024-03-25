<script lang="ts">
	import * as icons from 'lucide-svelte';
	export let name: string;
</script>

<svelte:component this={icons[name]} {...$$props} />
