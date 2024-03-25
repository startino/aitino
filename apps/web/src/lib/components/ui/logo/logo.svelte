<script lang="ts">
	export let height: string = 'h-9 w-9';

	export let label: boolean = false;
</script>

<div class="flex flex-row place-items-center gap-3">
	<img src="/logo/logo_nobg_nopadding.png" class="{$$props.class} {height} not-prose" alt="Logo" />

	{#if label}
		<span class="text-lg font-bold text-primary">Aitino</span>
	{/if}
</div>
