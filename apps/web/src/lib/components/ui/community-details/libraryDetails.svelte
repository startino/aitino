<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { User } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';
	import type { Agent, Crew } from '$lib/types/models';

	dayjs.extend(relativeTime);

	export let type: 'agent' | 'crew';
	export let displayedAgent: Agent | Crew;
	export let showDetails: boolean;
	const dispatch = createEventDispatcher();
	dayjs.extend(relativeTime);

	function closeDialog() {
		dispatch('close');
		showDetails = false;
		console.log(showDetails);
	}

	function timeSince(dateIsoString: Date | string | number) {
		return dayjs(dateIsoString).fromNow(true);
	}

	$: isAgent = type === 'agent';
	// Type assertion helpers
	$: agentItem = isAgent ? <Agent>displayedAgent : null;
	$: crewItem = !isAgent ? <Crew>displayedAgent : null;
</script>

<Dialog.Root open={showDetails} onOpenChange={() => closeDialog()}>
	<Dialog.Content
		class={type === 'agent'
			? 'h-5/6 w-full max-w-6xl space-y-8 overflow-y-auto rounded-lg p-8 shadow-2xl [&::-webkit-scrollbar]:hidden'
			: 'relativ bg-background max-w-5xl transform rounded-xl p-8 shadow-xl transition-all duration-500 ease-in-out hover:scale-105'}
	>
		{#if type === 'agent'}
			<div class="mb-8 flex flex-col items-center justify-center">
				<div class="relative">
					<img
						src={agentItem?.avatar}
						alt={agentItem?.title}
						class="border-primary h-48 w-48 rounded-full border-4 object-cover shadow-2xl"
					/>
					<div
						class="absolute -bottom-2 -right-2 animate-pulse rounded-full bg-blue-500 px-3 py-2 text-xs font-semibold text-white"
					>
						V {agentItem?.version}
					</div>
				</div>
				<div class="mt-4 flex flex-col items-center">
					{#if agentItem?.created_at}
						<p class="text-sm text-gray-400">Created {timeSince(agentItem?.created_at)}</p>
					{/if}
					<div
						class="mt-2 inline-flex items-center justify-center rounded-full bg-green-500 px-3 py-1 text-xs font-semibold text-white shadow"
					>
						Model: {agentItem?.model}
					</div>
				</div>
			</div>
			<div class="space-y-4 text-center">
				<h2
					class="bg-gradient-to-r from-blue-400 to-teal-300 bg-clip-text py-2 text-6xl font-extrabold text-transparent"
				>
					{agentItem?.title}
				</h2>
				<p class="mx-auto max-w-3xl text-xl text-gray-400">{agentItem?.role}</p>
				<!-- <p class="text-lg italic text-gray-500">— {agentItem?.author}</p> -->
			</div>

			<div class="text-white">
				<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Description</h3>
				<ul class="mt-4 list-inside list-disc space-y-2 text-gray-400">
					{#each agentItem.description as description}
						<li>{description}</li>
					{/each}
				</ul>
			</div>

			<div class="mt-6 text-white">
				<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Tools</h3>
				<div class="mt-4 flex flex-wrap gap-2">
					{#each agentItem.tools as tool}
						<span
							class="rounded-full bg-gray-700 px-4 py-2 text-sm transition-colors duration-200 hover:bg-gray-600"
							>{tool}</span
						>
					{/each}
				</div>
			</div>
		{:else}
			<div
				class="from-primary-950 to-primary-500 flex items-center justify-between rounded-t-2xl bg-gradient-to-r p-6"
			>
				<div class="flex items-center space-x-4">
					<div class="bg-primary-200 rounded-full p-1">
						<div class="bg-background rounded-full p-2">
							<User class="text-primary-500 h-12 w-12" />
						</div>
					</div>
					<div>
						<h2 class="text-on-primary text-xl font-bold">{crewItem?.title}</h2>
						<p class="text-on-primary/80 text-sm">Created {timeSince(crewItem.created_at)}</p>
					</div>
				</div>
			</div>
			<div class="text-on-surface mt-8 text-lg">{crewItem?.description}</div>
			<div class="mt-10">
				<h3 class="text-on-background mb-5 text-2xl font-semibold">Nodes</h3>
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
					{#each crewItem.nodes.filter((n) => n.type !== 'prompt') as node}
						<div
							class="from-surface-variant to-surface overflow-hidden rounded-lg bg-gradient-to-r shadow-lg transition duration-300 ease-in-out hover:shadow-2xl"
						>
							<div class="flex items-center p-4">
								<div class="mr-4 flex-shrink-0">
									<div class="border-primary h-16 w-16 overflow-hidden rounded-full border-2">
										<img
											src={node?.data.avatar || 'default-avatar.png'}
											alt=""
											class="h-full w-full object-cover"
										/>
									</div>
								</div>
								<div>
									<div class="text-primary font-semibold">{node?.data.name || 'Unnamed Node'}</div>
									<div class="text-secondary text-sm">Type: {node?.type}</div>
									{#if node?.data.model}
										<div class="text-tertiary text-sm">Model: {node?.data.model.label}</div>
									{/if}
									{#if node?.data.description}
										<div class="text-on-surface-variant mt-2 text-sm">{node?.data.description}</div>
									{/if}
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	</Dialog.Content>
</Dialog.Root>
