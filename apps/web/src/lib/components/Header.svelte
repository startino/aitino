<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, fly, slide } from 'svelte/transition';
	import { Button } from '$lib/components/ui/button';
	import Logo from './ui/logo/logo.svelte';

	export let pages: { [key: string]: string }[] = [
		{
			name: 'Home',
			href: '/'
		},
		{
			name: 'Features',
			href: '/#features-section'
		},
		{
			name: 'Benefits',
			href: '/#benefits-section'
		},
		{
			name: 'Pricing',
			href: '/#pricing-section'
		}
	];
	/** Labels and hrefs of CTA buttons on the hero. Recommended 1-2.*/
	export let CTAButtons: {
		[label: string]: { href: string; highlight: boolean };
	} = {};
	/**Property to determine if the class 'fixed' is applied to the header.*/
	export let sticky: boolean = true;

	// Constant Classes
	/** Default header class; user hasn't scrolled */
	let largeHeaderClass = `py-4 px-4 bg-card`;
	/** Class for when user has scrolled;  collapsed header */
	let miniHeaderClass = `py-2 px-2 md:py-4 md:px-4 bg-card`;

	// Variables
	let activeheaderClass = largeHeaderClass;
	let menuOpen = false;

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

	onMount(() => {
		window.addEventListener('scroll', () => {
			activeheaderClass = window.scrollY > 12 && sticky ? miniHeaderClass : largeHeaderClass;
		});
	});
</script>

<nav
	class="fixed left-1/2 mt-6 w-[90%] max-w-7xl -translate-x-1/2 items-center justify-between rounded-3xl bg-card px-6 py-3 text-card-foreground lg:flex lg:px-8 {menuOpen
		? 'hidden'
		: 'flex'}"
	aria-label="Global"
>
	<a href="/" class="-m-1.5 p-1.5">
		<span class="sr-only">Aitino</span>
		<Logo label />
	</a>

	<div class="flex lg:hidden">
		<button
			type="button"
			on:click={toggleMenu}
			class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
		>
			<span class="sr-only">Open main menu</span>
			<svg
				class="h-6 w-6"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				aria-hidden="true"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
				/>
			</svg>
		</button>
	</div>

	<div class="hidden place-items-center lg:flex lg:gap-x-12">
		{#each pages as { name, href }}
			<a
				{href}
				class="text-md m-0 font-semibold leading-6 text-card-foreground hover:text-accent sm:m-0"
				>{name}</a
			>
		{/each}
		<div class="grid {CTAButtons.length == 2 ? 'grid-cols-2' : 'grid-cols-1'} gap-x-4">
			{#each Object.entries(CTAButtons) as [name, { href, highlight }]}
				<Button {href} class="w-full">
					{name}
				</Button>
			{/each}
		</div>
	</div>
</nav>

{#if menuOpen}
	<!-- Mobile menu, show/hide based on menu open state. -->
	<div class="lg:hidden" role="dialog" aria-modal="true">
		<!-- Background backdrop, show/hide based on slide-over state. -->
		<div class="fixed inset-0 z-10" />
		<div
			class="fixed inset-y-0 right-0 z-50 w-full bg-card px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10"
			transition:fly={{ x: 400, y: 0, opacity: 1 }}
		>
			<div class="flex items-center justify-between">
				<a href="/" class="-m-1.5 p-1.5">
					<Logo label />
				</a>
				<button type="button" on:click={toggleMenu} class="-m-2.5 rounded-md p-2.5 text-gray-700">
					<span class="sr-only">Close menu</span>
					<svg
						class="h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="1.5"
						stroke="currentColor"
						aria-hidden="true"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>
			<div class="mt-6 flow-root">
				<div class="-my-6 divide-y divide-gray-500/10">
					<div class="space-y-2 py-6">
						{#each pages as { name, href }}
							<a
								{href}
								on:click={() => toggleMenu()}
								class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-card-foreground hover:bg-accent hover:text-accent-foreground"
								>{name}</a
							>
						{/each}
					</div>
					<div class="grid grid-cols-2 gap-x-4 py-6">
						{#each Object.entries(CTAButtons) as [name, { href, highlight }]}
							<Button {href} class="w-full" on:click={() => toggleMenu()}>
								{name}
							</Button>
						{/each}
					</div>
				</div>
			</div>
		</div>
	</div>
{/if}
