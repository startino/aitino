<script>
	import { cart } from '$lib/stores';
	import Icon from '../atoms/Icon.svelte';
</script>

<a
	href="/cart"
	class="flex flex-row bg-tertiary px-2 py-1 rounded-md gap-2 items-center align-text-top">
	<h1 class="body-large text-tertiary-on">
		{$cart.photos.length}
	</h1>

	<Icon icon="cart" fillColor="transparent" strokeColor="" class="stroke-tertiary-on" />
</a>
