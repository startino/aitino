<script lang="ts">
	import type { Agent } from '$lib/types/models';
	import { timeSince } from '$lib/utils';

	export let agentDisplayDetails: Agent;
</script>

<div class="mb-8 flex flex-col items-center justify-center">
	<div class="relative">
		<img
			src={agentDisplayDetails.avatar}
			alt={agentDisplayDetails.title}
			class="h-48 w-48 rounded-full border border-primary object-cover shadow-2xl"
		/>
		<div
			class="absolute -bottom-2 -right-2 animate-pulse rounded-full bg-blue-500 px-3 py-2 text-xs font-semibold text-white"
		>
			V {agentDisplayDetails.version}
		</div>
	</div>
	<div class="mt-4 flex flex-col items-center">
		{#if agentDisplayDetails.created_at}
			<p class="text-sm text-gray-400">Created {timeSince(agentDisplayDetails.created_at)}</p>
		{/if}
		<div
			class="mt-2 inline-flex items-center justify-center rounded-full bg-green-500 px-3 py-1 text-xs font-semibold text-white shadow"
		>
			Model: {agentDisplayDetails.model}
		</div>
	</div>
</div>
<div class="space-y-4 text-center">
	<h2
		class="bg-gradient-to-r from-blue-400 to-teal-300 bg-clip-text py-2 text-6xl font-extrabold text-transparent"
	>
		{agentDisplayDetails.title}
	</h2>
	<p class="mx-auto max-w-3xl text-xl text-gray-400">{agentDisplayDetails.role}</p>
</div>

<div class="text-white">
	<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Description</h3>
	<ul class="mt-4 list-inside list-disc space-y-2 text-gray-400">
		<!-- {#each agentDisplayDetails.description as description} -->
		<li>{agentDisplayDetails.description}</li>
		<!-- {/each} -->
	</ul>
</div>

<div class="mt-6 text-white">
	<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Tools</h3>
	<div class="mt-4 flex flex-wrap gap-2">
		{#each agentDisplayDetails.tools as tool}
			<span
				class="rounded-full bg-gray-700 px-4 py-2 text-sm transition-colors duration-200 hover:bg-gray-600"
				>{tool}</span
			>
		{/each}
	</div>
</div>
