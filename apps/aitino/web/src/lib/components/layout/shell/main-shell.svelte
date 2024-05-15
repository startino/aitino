<script lang="ts">
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';
	// Slots
	/** @slot header - Insert fixed header content, such as Skeleton's App Bar component.
	 * @slot sidebarLeft - Hidden when empty. Allows you to set fixed left sidebar content.
	 * @slot sidebarRight - Hidden when empty. Allows you to set fixed right sidebar content.
	 * @slot pageHeader - Insert content that resides above your page content. Great for global alerts.
	 * @slot pageFooter - Insert content that resides below your page content. Recommended for most layouts.
	 * @slot footer - Insert fixed footer content. Not recommended for most layouts.
	 */

	// Types to get TailwindCSS Intellisense
	import type { SvelteEvent } from '$lib/types';

	interface $$Events {
		scroll: SvelteEvent<UIEvent, HTMLDivElement>;
	}

	// Props
	/** Set `scrollbar-gutter` style. */
	export let scrollbarGutter = 'auto';

	// Props (regions)
	/** Apply arbitrary classes to the entire `#page` region. */
	export let regionPage: string = '';
	/** Apply arbitrary classes to the `header` slot container element */
	export let slotHeader: string = 'z-10';
	/** Apply arbitrary classes to the `sidebarLeft` slot container element */
	export let slotSidebarLeft: string = 'w-auto';
	/** Apply arbitrary classes to the `sidebarRight` slot container element */
	export let slotSidebarRight: string = 'w-auto';
	/** Apply arbitrary classes to the `pageHeader` slot container element */
	export let slotPageHeader: string = '';
	/** Apply arbitrary classes to the `pageContent` slot container element */
	export let slotPageContent: string = '';
	/** Apply arbitrary classes to the `pageFooter` slot container element */
	export let slotPageFooter: string = '';
	/** Apply arbitrary classes to the `footer` slot container element */
	export let slotFooter: string = '';

	// Base classes
	const cBaseAppShell: string = 'w-full h-full flex flex-col overflow-hidden';
	const cContentArea: string = 'w-full h-full flex overflow-hidden';
	const cPage: string = 'flex-1 overflow-x-hidden flex flex-col ';
	const cSidebarLeft: string = 'flex-none overflow-x-hidden overflow-y-auto';
	const cSidebarRight: string = 'flex-none overflow-x-hidden overflow-y-auto';

	// Reactive Classes
	$: classesBase = `${cBaseAppShell} ${$$props.class ?? ''}`;
	$: classesHeader = `${slotHeader}`;
	$: classesSidebarLeft = `${cSidebarLeft} ${slotSidebarLeft}`;
	$: classesSidebarRight = `${cSidebarRight} ${slotSidebarRight}`;
	$: classesPageHeader = `${slotPageHeader}`;
	$: classesPageContent = `${slotPageContent}`;
	$: classesPageFooter = `${slotPageFooter}`;
	$: classesFooter = `${slotFooter}`;
	let mounted = false;
	onMount(() => {
		mounted = true;
	});
</script>

<div id="appShell" class={classesBase} data-testid="app-shell">
	<!-- Slot: Header -->
	{#if $$slots.header}
		<header
			class:invisible={!mounted}
			id="shell-header"
			class="flex-none {classesHeader} {mounted ? 'opacity-100' : 'opacity-0'} transition-opacity"
		>
			<slot name="header" />
		</header>
	{/if}

	<!-- Content Area -->
	<div
		class:invisible={!mounted}
		class="flex-auto {mounted
			? 'opacity-100'
			: 'opacity-0'} transition-opacity duration-300 {cContentArea}"
	>
		<!-- Slot: Sidebar (left) -->
		{#if $$slots.sidebarLeft}
			<aside id="sidebar-left" class={classesSidebarLeft}>
				<slot name="sidebarLeft" />
			</aside>
		{/if}

		<!-- Page -->
		<div id="page" class="{regionPage} {cPage}" style:scrollbar-gutter={scrollbarGutter} on:scroll>
			<!-- Slot: Page Header -->
			{#if $$slots.pageHeader}
				<header id="page-header" class="flex-none {classesPageHeader}">
					<slot name="pageHeader">(slot:header)</slot>
				</header>
			{/if}

			<!-- Slot: Page Content (default) -->
			<main id="page-content" class="flex-auto {classesPageContent}">
				<slot />
			</main>

			<!-- Slot: Page Footer -->
			{#if $$slots.pageFooter}
				<footer id="page-footer" class="flex-none {classesPageFooter}">
					<slot name="pageFooter">(slot:footer)</slot>
				</footer>
			{/if}
		</div>

		<!-- Slot: Sidebar (right) -->
		{#if $$slots.sidebarRight}
			<aside id="sidebar-right" class={classesSidebarRight}>
				<slot name="sidebarRight" />
			</aside>
		{/if}
	</div>

	<!-- Slot: footer -->
	{#if $$slots.footer}
		<footer id="shell-footer" class="flex-none {classesFooter}">
			<slot name="footer" />
		</footer>
	{/if}
</div>
