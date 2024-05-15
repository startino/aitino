<script lang="ts">
	export let searchInput;
	import Icon from '$lib/components/atoms/Icon.svelte';
</script>

<label for="search-field" class="mb-2 text-sm font-medium text-gray-900 sr-only text-gray-300"
	>Search</label>
<div class="relative">
	<input
		type="text"
		id="search-field"
		bind:value={searchInput}
		class="block p-4 pl-6 w-full title-medium  text-surface-on  rounded-lg border  border-outline focus: focus: bg-surface placeholder-surface-on focus:ring-tertiary focus:border-tertiary"
		placeholder="Search Name, Date, Album..."
		on:input />
	<!-- <button
		type="submit"
		class="absolute right-2.5 bottom-2.5  bg-primary focus:ring-4 focus:outline-none focus: font-medium rounded-lg text-sm px-4 py-2 hover:bg-tertiary focus:ring-tertiary"
	>
		<Icon icon="search" />
	</button> -->
</div>
