<script lang="ts">
	import { newPhoto, type PhotoType } from '$lib/components/photoType';
	import { cart, alerts, resetCart } from '$lib/stores.js';
	import Icon from '../atoms/Icon.svelte';
	import type { PhotoData } from '../photoDatum';
	export let photoData: PhotoData;
	const addToCart = (photoData) => {
		let photo = newPhoto(photoData);
		$cart.photos = [...$cart.photos, photo];
		$cart.total += photoData.price;
		console.log($cart);
		alerts.addedToCart('Added To Cart!', 2000);
	};
</script>

<button on:click={() => addToCart(photoData)} class="bg-tertiary rounded-lg">
	<Icon icon="cart" class="stroke-tertiary-on p-2" strokeColor="" />
</button>
