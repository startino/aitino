<script lang="ts">
	import '$styling';
	import { setContext } from 'svelte';
	import { Shell } from '$lib/components/layout/shell';
	import Header from '$lib/components/Header.svelte';
	import Footer from '$lib/components/Footer.svelte';

	export let data;

	setContext('splitTestIdentifier', data?.splitTestIdentifier);

	export let CTAButtons: {
		[label: string]: { href: string; highlight: boolean };
	} = {
		'Sign In': { href: '/register', highlight: true }
	};
</script>

<Shell>
	<svelte:fragment slot="header">
		<Header {CTAButtons} />
	</svelte:fragment>
	<svelte:fragment slot="sidebarLeft"></svelte:fragment>
	<svelte:fragment slot="pageHeader"></svelte:fragment>
	<!-- Router Slot -->
	<div class="overflow-y-hidden"><slot /></div>

	<!-- ---- / ---- -->
	<svelte:fragment slot="pageFooter"></svelte:fragment>
	<!-- (footer) -->
	<svelte:fragment slot="footer"><Footer /></svelte:fragment>
</Shell>
