<script lang="ts">
	import Header from '$lib/components/organisms/Header.svelte';
	import { newPhoto, type PhotoType } from '$lib/components/photoType';
	import { cart } from '$lib/stores';
	import RemoveFromCart from '$lib/components/molecules/RemoveFromCart.svelte';
	import { photoDatum, type PhotoData } from '$lib/components/photoDatum';
	import Photo from '../shop/Photo.svelte';

	type displayItem = {
		photoData: PhotoData;
		count: number;
	};

	let displayCart: displayItem[] = [];

	const updateDisplayCart = () => {
		displayCart = [];

		photoDatum.forEach((photoData) => {
			let count = 0;
			$cart.photos.forEach((photo) => {
				if (photo.label == photoData.label) {
					count++;
				}
			});
			if (count > 0) {
				displayCart.push({
					photoData: photoData,
					count: count,
				});
			}
		});
	};

	let unsubscribeCart = cart.subscribe((currentValue) => {
		console.log('Updating Display Cart');
		updateDisplayCart();
	});

	function checkout() {
		// Just for convenience until we actual checkout setup.
		cart.reset();
	}
</script>

<Header />
<main class="my-32 mx-3 flex flex-col gap-8 items-center mb-44">
	{#if displayCart.length == 0}
		<h1 class="title-medium">Your Cart is Empty.</h1>
		<a href="/shop" class="title-medium underline-animation"
			>You can click on me to go to the shop.</a>
	{/if}

	{#each displayCart as { photoData, count }}
		<div class="flex flex-row items-center gap-3 bg-surface-variant rounded-md max-w-3xl">
			<img src={photoData.path} alt="" class="w-[20%] aspect-square rounded-l-md" />
			<div
				class="text-center text-surface-variant-on flex flex-row justify-between px-2 md:px-4 gap-x-3 pr-3 items-center w-full">
				<div class="flex flex-col text-left">
					<h1 class="title-medium">
						<span class="block">
							{photoData.label}
						</span>
					</h1>
					<h1 class="body-medium ">{photoData.album}</h1>
				</div>
				<h1 class="title-large ">${photoData.price}</h1>
				<h1 class="title-large ">{count}</h1>
				<RemoveFromCart {photoData} />
			</div>
		</div>
	{/each}

	<button
		class="fixed bottom-0 mb-8 md:mb-14 m-6 rounded-md mx-auto {displayCart.length == 0
			? 'bg-surface-variant/30 text-red-700 hover:cursor-not-allowed'
			: 'bg-secondary-container'}"
		on:click={() => checkout()}>
		<h1 class="headline-medium py-3 px-12 text-secondary-container-on">Proceed To Checkout</h1>
	</button>
</main>
