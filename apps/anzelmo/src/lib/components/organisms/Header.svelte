<script lang="ts">
	import { base } from '$app/paths';

	import Logo from '$lib/components/atoms/Logo.svelte';
	import { fly, slide } from 'svelte/transition';
	import process from 'node:process';
	import { onMount } from 'svelte';
	import Alert from '$lib/components/molecules/Alert.svelte';
	import Icon from '../atoms/Icon.svelte';
	import { cart } from '$lib/stores';
	import CartButton from '../molecules/CartButton.svelte';

	export let burgerOpen = false;

	const headerItems = [
		{
			label: 'Gallery',
			href: '/',
		},
		{
			label: 'Cart',
			href: '/cart',
		},
		{
			label: 'Shop',
			href: '/shop',
		},
		{
			label: 'Blog',
			href: '/blog',
		},
		{
			label: 'About',
			href: '/about',
		},
		{
			label: 'Contact',
			href: '/contact',
		},
	];

	const toggleMenu = () => {
		burgerOpen = !burgerOpen;
	};
</script>

<div
	id="header"
	class="{$$props.class} border-b border-transparent fixed top-0 z-40 flex-none w-full transition-all duration-400">
	<div class="py-6 px-4 md:px-10 lg:px-24">
		<div class="flex relative items-center justify-between">
			<!--Logo-->
			<a class="flex flex-row px-3 gap-3 justify-center items-center" href="{base}/">
				<Logo />
				<p class="hidden pt-0.5 text-lg font-bold md:flex">Anzelmo</p>
			</a>
			<!--Cart-->

			<div class="md:hidden">
				<CartButton />
			</div>

			<div class="relative md:hidden text-right">
				<button
					on:click={() => {
						toggleMenu();
					}}
					type="button"
					class="inline-flex items-center p-2 ml-1 stroke-outline rounded-lg transition-transform bg-transparent  {burgerOpen
						? 'rotate-90'
						: ''}">
					{#if burgerOpen}
						<Icon icon="burgur" />
					{:else}
						<Icon icon="cross" />
					{/if}
				</button>
				<!--Mobile header's nav list-->
				{#if burgerOpen}
					<nav
						class="absolute flex flex-col right-0 text-left py-2 rounded-lg"
						in:fly={{ x: 300 }}
						out:fly={{ x: 300 }}>
						<ul class="flex flex-col gap-y-3 items-center bg-surface rounded-lg">
							<Alert />
							{#each headerItems as { label, href }}
								<li>
									<a class="inline hover:text-tertiary" {href}>
										<h1 class="body-medium px-16 py-2 underline-animation">
											{label}
										</h1>
									</a>
								</li>
							{/each}
						</ul>
					</nav>
				{/if}
			</div>

			<nav class="ml-auto body-large hidden items-center w-full md:flex md:w-auto md:order-1 z-10">
				<ul class="flex space-x-8 relative items-center">
					<Alert />
					{#each headerItems as { label, href }}
						<li>
							<a
								class="inline hover:text-tertiary underline-animation"
								{href}>
								{label}
							</a>
						</li>
					{/each}

					<li class="w-fit">
						<CartButton />
					</li>
					<li
						class="border-l  border-secondary/50 self-stretch" />

					<li>

					</li>
				</ul>
			</nav>
		</div>
	</div>
</div>
