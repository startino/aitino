<script lang="ts">
	import { base } from '$app/paths';
	import Header from '$lib/components/organisms/Header.svelte';
	import Footer from '$lib/components/organisms/Footer.svelte';
	import { photoDatum, type PhotoData } from '$lib/components/photoDatum';
	import Icon from '$lib/components/atoms/Icon.svelte';
	import Photo from './Photo.svelte';
	import NoResults from './NoResults.svelte';
	import SearchBox from './SearchBox.svelte';
	import AddToCart from '$lib/components/molecules/AddToCart.svelte';

	let filteredPhotos: PhotoData[] = [];

	// For Search Input
	let searchInput = '';

	// Matches photoData
	const searchPhotos = () => {
		return (filteredPhotos = photoDatum.filter((photoData) => {
			if (photoData.label.toLowerCase().includes(searchInput.toLowerCase())) return true;
			if (photoData.album.toLowerCase().includes(searchInput.toLowerCase())) return true;
		}));
	};
</script>

<Header />

<main class="pt-32 px-6 md:px-12 lg:px-24 w-full">
	<div class="flex flex-col">
		<SearchBox bind:searchInput on:input={searchPhotos} />
		{#if searchInput && filteredPhotos.length === 0}
			<NoResults />
		{:else if filteredPhotos.length > 0}
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 py-12">
				{#each filteredPhotos as photoData}
					<Photo {photoData} />
				{/each}
			</div>
		{:else}
			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-12 py-12">
				{#each photoDatum as photoData}
					<Photo {photoData} />
					<Photo {photoData} />
					<Photo {photoData} />
				{/each}
			</div>
		{/if}
	</div>
</main>
