<script lang="ts">
	import type { Crew } from '$lib/types/models';
	import { timeSince } from '$lib/utils';

	export let crewDisplayDetails: Crew;
</script>

<div
	class="flex items-center justify-between rounded-t-2xl bg-gradient-to-r from-primary-950 to-primary-500 p-6"
>
	<div class="flex items-center space-x-4">
		<div class="rounded-full bg-primary-200 p-1">
			<div class="flex h-20 w-20 items-center justify-center rounded-full">
				<img
					src={crewDisplayDetails.avatar}
					alt={crewDisplayDetails.title}
					class="rounded-full object-cover shadow-2xl"
				/>
			</div>
		</div>
		<div>
			<h2 class="text-on-primary text-xl font-bold">{crewDisplayDetails.title}</h2>
			<p class="text-on-primary/80 text-sm">Created {timeSince(crewDisplayDetails.created_at)}</p>
		</div>
	</div>
</div>
<div class="text-on-surface mt-8 text-lg">{crewDisplayDetails?.description}</div>
<div class="mt-10">
	<h3 class="text-on-background mb-5 text-2xl font-semibold">Nodes</h3>
	<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
		{#each crewDisplayDetails.nodes.filter((n) => n.type !== 'prompt') as node}
			<div
				class="overflow-hidden rounded-lg bg-gradient-to-r from-surface-variant to-surface shadow-lg transition duration-300 ease-in-out hover:shadow-2xl"
			>
				<div class="flex items-center p-4">
					<div class="mr-4 flex-shrink-0">
						<div class="h-16 w-16 overflow-hidden rounded-full border-2 border-primary">
							<img
								src={node.data.avatar || 'default-avatar.png'}
								alt=""
								class="h-full w-full object-cover"
							/>
						</div>
					</div>
					<div>
						<div class="font-semibold text-primary">{node.data.name || 'Unnamed Node'}</div>
						<div class="text-sm text-secondary">Type: {node.type}</div>
						{#if node.data.model}
							<div class="text-sm text-tertiary">Model: {node.data.model.label}</div>
						{/if}
						{#if node.data.description}
							<div class="text-on-surface-variant mt-2 text-sm">{node.data.description}</div>
						{/if}
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>
