<script lang="ts">
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { Button } from '$lib/components/ui/button';
	import { Pickaxe, Check, CheckCheck, Ban, CircleHelp } from 'lucide-svelte';

	export let status: string;
</script>

<div class=" [&>*]:mx-auto [&>*]:h-6 [&>*]:w-6">
	{#if status == 'under_review'}
		<Pickaxe class="text-yellow-500" />
	{:else if status == 'subscriber'}
		<Check class="text-emerald-400" />
	{:else if status == 'rejected'}
		<Ban class="text-red-500" />
	{:else if status == 'subscriber'}
		<CheckCheck class="text-emerald-400" />
	{:else}
		<CircleHelp class="text-blue-500" />
	{/if}
</div>
