<script lang="ts">
	import { alerts } from '$lib/stores.js';
	import { onDestroy } from 'svelte';
	import { fly, slide } from 'svelte/transition';

	export let duration = 1000;
	let visible: boolean;
	let timeout;
</script>

<div class="flex flex-col justify-items-start absolute top-full right-0 py-6 gap-3">
	{#each $alerts as alert (alert.id)}
		<div class="bg-tertiary w-fit p-6 rounded-md" transition:fly={{ y: 30 }}>
			<div class="content">
				<h1 class="title-medium text-tertiary-on">
					{alert.message}
				</h1>
			</div>
		</div>
	{/each}
</div>
