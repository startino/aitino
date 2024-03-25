<script lang="ts">
	import { getContext } from '$lib/utils';
	import type { PanelAction } from '$lib/types';
	import { Button } from '$lib/components/ui/button';
	import { AGENT_LIMIT, PROMPT_LIMIT } from '$lib/config';

	export let actions: PanelAction[] = [];
	export let title: string;
	export let description: string;

	const { count } = getContext('crew');
</script>

<!-- Static sidebar for desktop -->
<div
	class="hidden h-full overflow-y-clip rounded-2xl border bg-primary-900/50 p-6 lg:z-50 lg:grid lg:w-72"
>
	<div class="mb-4 grid">
		<h1 contenteditable on:input={(e) => (title = e.target.innerText)}>
			{title}
		</h1>
		<p
			contenteditable
			class="text-sm text-gray-300"
			on:input={(e) => (description = e.target.innerText)}
		>
			{description}
		</p>
	</div>
	<!-- Sidebar component, swap this element with another sidebar if you like -->
	<ul role="list" class="mb-6 grid w-full gap-2">
		{#each actions as action}
			<li class="grid">
				{#if action.isCustom}
					<slot {action}>
						{action.name}
					</slot>
				{:else}
					<Button on:click={action.onclick} variant={action.buttonVariant} class="w-full">
						{action.name}
					</Button>
				{/if}
			</li>
		{/each}
	</ul>

	<ul>
		<li>{$count.prompts} / {PROMPT_LIMIT} prompts</li>
		<li>{$count.agents} / {AGENT_LIMIT} agents</li>
	</ul>
</div>
