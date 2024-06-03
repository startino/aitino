<script>
	import Render from './Render.svelte';
	export let instance = void 0;
	export let config;
	export let props = void 0;
</script>

{#if config.children.length === 0}
	<svelte:component this={config.component} bind:this={instance} {...props ?? {}} />
{:else}
	<svelte:component this={config.component} bind:this={instance} {...props ?? {}}>
		{#each config.children as child}
			<Render of={child} />
		{/each}
	</svelte:component>
{/if}
