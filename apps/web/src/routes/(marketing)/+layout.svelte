<script lang="ts">
	import { page } from '$app/stores';
	import '$styling';
	import { Toaster } from 'svelte-sonner';
	import { setContext } from 'svelte';
	import { Shell } from '$lib/components/layout/shell';
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';

	export let data;

	setContext('splitTestIdentifier', data?.splitTestIdentifier);

	export let CTAButtons: {
		[label: string]: { href: string; highlight: boolean };
	} = {
		'Sign In': { href: '#', highlight: true, disabled: true }
	};
</script>

<div
	class="sunset-banner sticky top-0 z-50 border-b border-destructive bg-destructive/10 p-4 text-center font-semibold"
>
	⚠️ This project has been sunset and is no longer actively maintained.
</div>

<Shell>
	<svelte:fragment slot="header">
		<Header {CTAButtons} disabled={true} />
	</svelte:fragment>
	<svelte:fragment slot="sidebarLeft"></svelte:fragment>
	<svelte:fragment slot="pageHeader"></svelte:fragment>
	<!-- Router Slot -->
	<div class="overflow-y-hidden"><slot /></div>

	<!-- ---- / ---- -->
	<svelte:fragment slot="pageFooter"></svelte:fragment>
	<!-- (footer) -->
	<svelte:fragment slot="footer"><Footer disabled={true} /></svelte:fragment>
</Shell>

<footer class="border-t border-border/40 bg-background">
	<div
		class="container flex flex-col items-center justify-between gap-4 py-10 md:h-24 md:flex-row md:py-0"
	>
		<div class="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
			<span class="text-center text-sm text-muted-foreground md:text-left">
				© {new Date().getFullYear()} Aitino. All rights reserved.
			</span>
		</div>
		<div class="flex gap-4">
			{#each ['Terms', 'Privacy', 'Contact'] as item}
				<span class="cursor-not-allowed text-sm text-foreground/50">{item}</span>
			{/each}
		</div>
	</div>
</footer>

<Toaster />

<style>
	.sunset-banner {
		position: sticky;
		top: 0;
		z-index: 50;
	}
</style>
