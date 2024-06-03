<script lang="ts">
	export let height: string = 'h-9 w-9';

	export let label: boolean = false;
</script>

<div class="flex flex-row place-items-center gap-3">
	<img src="/favicon.png" class="{$$props.class} {height} not-prose" alt="Logo" />

	{#if label}
		<span class="text-primary text-lg font-bold">Rest</span>
	{/if}
</div>
