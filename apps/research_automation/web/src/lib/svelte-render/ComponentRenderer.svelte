<script>
	import { onMount } from 'svelte';
	import { Subscribe } from 'svelte-subscribe';
	import PropsRenderer from './PropsRenderer.svelte';
	import { isReadable } from './store.js';
	export let config;
	let instance;
	onMount(function attachEventHandlers() {
		config.eventHandlers.forEach(([type, handler]) => {
			const callbacks = instance.$$.callbacks[type] ?? [];
			callbacks.push(handler);
			instance.$$.callbacks[type] = callbacks;
		});
		return function detachEventHandlers() {
			config.eventHandlers.forEach(([type, handler]) => {
				const callbacks = instance.$$.callbacks[type];
				const idx = callbacks.findIndex((c) => c === handler);
				callbacks.splice(idx, 1);
			});
		};
	});
</script>

{#if isReadable(config.props)}
	<Subscribe props={config.props} let:props>
		<PropsRenderer bind:instance {config} {props} />
	</Subscribe>
{:else}
	<PropsRenderer bind:instance {config} props={config.props} />
{/if}
