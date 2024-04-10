<script lang="ts">
	import { SvelteFlowProvider } from '@xyflow/svelte';
	import { setContext } from 'svelte';
	import { writable } from 'svelte/store';

	setContext('crew', {
		receiver: writable(null),
		count: writable({ agents: 0, prompts: 0 })
	});
</script>

<SvelteFlowProvider>
	<slot />
</SvelteFlowProvider>
