<script lang="ts">
	import { base } from '$app/paths';
	import Header from '$lib/components/organisms/Header.svelte';
	import Footer from '$lib/components/organisms/Footer.svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	const albums = [
		{
			index: 0,
			date: '2022',
			name: 'Album Name Zero',
			coverImgPath: 'temp_photography/photo1.jpg',
		},
		{
			index: 1,
			date: '2020',
			name: 'Album Name One',
			coverImgPath: 'temp_photography/photo2.jpg',
		},
		{
			index: 2,
			date: '2020',
			name: 'Album Name Two',
			coverImgPath: 'temp_photography/photo3.jpg',
		},
		{
			index: 3,
			date: '2019',
			name: 'Album Name Three',
			coverImgPath: 'temp_photography/photo4.jpg',
		},
		{
			index: 4,
			date: '2014',
			name: 'Album Name Four',
			coverImgPath: 'temp_photography/photo1.jpg',
		},
		{
			index: 5,
			date: '2014',
			name: 'Album Name Five',
			coverImgPath: 'temp_photography/photo1.jpg',
		},
	];

	let currentImgPath: string = albums[0].coverImgPath;
	let currentIndex: number = 0;
	let selectedImgPath: string = albums[0].coverImgPath;

	function updateBackgroundImage(newIndex: number) {
		currentIndex = newIndex;
		currentImgPath = albums[currentIndex].coverImgPath;
		//	console.log('current img path: ', currentImgPath);
	}

	function handleClick(index: number) {
		// Go to
	}
	function mouseEnter(index: number) {
		currentIndex = index;
		updateBackgroundImage(index);
	}

	$: currentImgPath = albums[currentIndex].coverImgPath;

	let albumHeight: number = 0;

	let scrollY: number = 0;

	function calculateBgImage() {
		let index: number;

		index = Math.round((scrollY - 200) / albumHeight);
		index = index < 0 || index >= albums.length ? 0 : index;

		updateBackgroundImage(index);
	}

	$: scrollY, calculateBgImage();
</script>

<svelte:window bind:scrollY />

<Header />

<main class="text-center md:text-left flex flex-col items-stretch">
	<!-- <div in:fade class="w-full h-full bg-[url({currentImgPath})] bg-cover bg-center fixed" /> -->
	{#key currentImgPath}
		<img
			transition:fade={{ duration: 300 }}
			src={currentImgPath}
			alt=""
			class="w-full h-full bg-center object-cover fixed" />
	{/key}

	<!--Hero-->
	<section
		id="hero"
		class="grow py-32 h-screen sm:py-34 md:py-44 px-4 md:pl-16 lg:pl-32 grid space-y-12 relative">
		<div class="grid h-fit w-fit self-center flex-col gap-y-24 pb-48">
			{#each albums as { index, date, name, coverImgPath }}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div
					bind:clientHeight={albumHeight}
					class="flex flex-col my-12 group hover:cursor-pointer underline-animation"
					on:click={(event) => handleClick(index)}
					on:mouseenter={(event) => mouseEnter(index)}>
					{#if index == currentIndex}
						<h1 class="headline-large text-white">{date}</h1>
						<h1 class="display-large text-white">
							{name}
						</h1>
					{:else}
						<h1 class="headline-large text-white/50">{date}</h1>
						<h1 class="display-large underline-animation text-white/50">
							{name}
						</h1>
					{/if}
				</div>
			{/each}
		</div>
	</section>
</main>
