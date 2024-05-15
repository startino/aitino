<script lang="ts">
	import AddToCart from '$lib/components/molecules/AddToCart.svelte';

	import type { PhotoData } from '$lib/components/photoDatum';
	import type { PhotoType } from '$lib/components/photoType';
	import { onMount } from 'svelte';
	export let photoData: PhotoData;

	let elementCentered: boolean = false;

	// This could probably be optimized by adding one observer in shop and looping through all of them instead of just [0].. but like.. yk..
	// Also, a timer should probably be used to prevent "repeated intersection by enlarging".
	// Also using it as a component instead of an action is more optimized but.. yk..
	function inView(node: Element, params = {}) {
		let observer: IntersectionObserver;

		const handleIntersect = (entry: IntersectionObserverEntry[]) => {
			entry[0].isIntersecting ? (elementCentered = true) : (elementCentered = false);
		};

		const setObserver = () => {
			const marginTop: number = -30;
			const marginBottom: number = -30;
			const rootMargin: string = `${marginTop}% 0% ${marginBottom}% 0%`;
			const options = { rootMargin, threshold: 0.6 };
			if (observer) observer.disconnect();
			observer = new IntersectionObserver(handleIntersect, options);
			observer.observe(node);
		};

		setObserver();

		return {
			update() {
				setObserver();
			},

			destroy() {
				if (observer) observer.disconnect();
			},
		};
	}
</script>

<div
	use:inView
	class="flex flex-col transition duration-700 md:duration:400 md:hover:scale-110 {elementCentered
		? 'scale-105 md:scale-100'
		: 'scale-95 md:scale-100'}"
	style={elementCentered ? 'atransform: scale(1.05)' : ''}>
	<a href="/shop" class=""> <img src={photoData.path} alt="" class="object-contain" /></a>

	<div class="flex w-full flex-row place-items-center gap-4 uppercase justify-between py-2">
		<a href="/shop" class="flex flex-col text-left">
			<h1 class="title-small font-thin">{photoData.album}</h1>
			<h1 class="headline-small text-surface-variant-on font-semibold underline-animation">
				{photoData.label}
			</h1>
		</a>
		<div class="flex flex-col place-items-center p-2 gap-1">
			<AddToCart {photoData} />
			<h1 class="title-large text-center">${photoData.price}</h1>
		</div>
	</div>
</div>
