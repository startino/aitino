<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { User } from 'lucide-svelte';
	import type { Crew } from '$lib/types/models';
	import { createEventDispatcher } from 'svelte';
	import dayjs from 'dayjs';
	import relativeTime from 'dayjs/plugin/relativeTime';

	export let displayedAgent: Crew;
	export let showDetails: boolean;
	const dispatch = createEventDispatcher();
	dayjs.extend(relativeTime);

	function closeDialog() {
		dispatch('close');
		showDetails = false;
		console.log(showDetails);
	}

	function timeSince(dateIsoString: Date) {
		return dayjs(dateIsoString).fromNow(true);
	}
</script>

<div class="mx-auto max-w-6xl px-4 py-8">
	<Dialog.Root open={showDetails} onOpenChange={() => closeDialog()}>
		<Dialog.Content
			class="relativ bg-background max-w-5xl transform rounded-xl p-8 shadow-xl transition-all duration-500 ease-in-out hover:scale-105"
		>
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
						<h2 class="text-on-primary text-xl font-bold">{displayedAgent.title}</h2>
						<p class="text-on-primary/80 text-sm">Created {timeSince(displayedAgent.created_at)}</p>
					</div>
				</div>
			</div>
			<div class="text-on-surface mt-8 text-lg">{displayedAgent.description}</div>
			<div class="mt-10">
				<h3 class="text-on-background mb-5 text-2xl font-semibold">Nodes</h3>
				<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
					{#each displayedAgent.nodes.filter((n) => n.type !== 'prompt') as node}
						<div
							class="from-surface-variant to-surface overflow-hidden rounded-lg bg-gradient-to-r shadow-lg transition duration-300 ease-in-out hover:shadow-2xl"
						>
							<div class="flex items-center p-4">
								<div class="mr-4 flex-shrink-0">
									<div class="border-primary h-16 w-16 overflow-hidden rounded-full border-2">
										<img
											src={node.data.avatar || 'default-avatar.png'}
											alt=""
											class="h-full w-full object-cover"
										/>
									</div>
								</div>
								<div>
									<div class="text-primary font-semibold">{node.data.name || 'Unnamed Node'}</div>
									<div class="text-secondary text-sm">Type: {node.type}</div>
									{#if node.data.model}
										<div class="text-tertiary text-sm">Model: {node.data.model.label}</div>
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
		</Dialog.Content>
	</Dialog.Root>
</div>
