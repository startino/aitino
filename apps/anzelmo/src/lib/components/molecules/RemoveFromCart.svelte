<script lang="ts">
	import type { PhotoType } from '$lib/components/photoType';
	import { alerts, cart } from '$lib/stores.js';
	import type { PhotoData } from '../photoDatum';
	export let photoData: PhotoData;
	const removeFromCart = () => {
		// Gets first photo of the label specified.
		let chosen_id: number;

		$cart.photos.forEach((photo) => {
			if (photo.label == photoData.label) {
				chosen_id = photo.id;
			}
		});

		$cart.photos = $cart.photos.filter((photo) => photo.id !== chosen_id);
		$cart.total -= photoData.price;
	};
</script>

<button on:click={() => removeFromCart()} class="rounded-md bg-secondary">
	<h1 class="body-large p-2 text-secondary-on">Remove</h1></button>
