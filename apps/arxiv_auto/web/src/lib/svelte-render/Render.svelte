<script>
	import ComponentRenderer from './ComponentRenderer.svelte';
	import { isReadable, Undefined } from './store.js';
	let config;
	export { config as of };
	const readableConfig = isReadable(config) ? config : Undefined;
</script>

{#if isReadable(config)}
	<!-- Auto-subscription must be on a non-nullable `Readable`. -->
	{$readableConfig}
	<p/>
{:else if typeof config !== 'object'}
	{config}
{:else}
	<ComponentRenderer {config} />
{/if}
