<script lang="ts">
	let scrollY: number;
	let index: number;

	$: scrollY, calculateIndex();

	function calculateIndex() {
		index = Math.round((scrollY - 200) / 336);
	}
</script>

<svelte:window bind:scrollY />
<div class="divide-y-2">
	<div class="fixed mx-32">
		{scrollY}
		index {index}
	</div>
	<div class="h-1 bg-red-700 w-full top-[333px] fixed" />
	<div class="h-[200px] bg-black" />
	{#each Array(10) as item, i}
		<div class="h-[332px] my-1 w-24 bg-primary text-black relative">
			<div class="absolute">
				{i}
			</div>
			<div class="h-1 bg-green-500 w-full top-[40%] absolute" />
			<div class="h-2 bg-blue-500 w-full top-1/2 absolute" />
			<div class="h-1 bg-green-500 w-full top-[40%] absolute" />
		</div>
	{/each}
</div>
