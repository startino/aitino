<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { User } from 'lucide-svelte';
	import type { Agent } from '$lib/types/models';
	import { createEventDispatcher } from 'svelte';

	export let displayedAgent: Agent;
	export let showDetails: boolean;
	const dispatch = createEventDispatcher();

	function closeDialog() {
		dispatch('close');
		showDetails = false
		console.log(showDetails);
	}

	function timeSince(dateIsoString: string | number | Date) {
		const date = new Date(dateIsoString);
		const now = new Date();
		const diffInSeconds = Math.round((now - date) / 1000);

		if (diffInSeconds < 60) {
			return 'just now';
		} else if (diffInSeconds < 3600) {
			return `${Math.floor(diffInSeconds / 60)} minute${Math.floor(diffInSeconds / 60) === 1 ? '' : 's'} ago`;
		} else if (diffInSeconds < 86400) {
			return `${Math.floor(diffInSeconds / 3600)} hour${Math.floor(diffInSeconds / 3600) === 1 ? '' : 's'} ago`;
		} else if (diffInSeconds < 172800) {
			return 'yesterday';
		} else if (diffInSeconds < 2592000) {
			return `${Math.floor(diffInSeconds / 86400)} day${Math.floor(diffInSeconds / 86400) === 1 ? '' : 's'} ago`;
		} else if (diffInSeconds < 31104000) {
			const months = Math.floor(diffInSeconds / 2592000);
			if ([1, 2, 3, 6].includes(months)) {
				return `${months} month${months === 1 ? '' : 's'} ago`;
			}
			return `${months} months ago`;
		} else {
			const years = Math.floor(diffInSeconds / 31104000);
			return `${years} year${years === 1 ? '' : 's'} ago`;
		}
	}
</script>

<div class="mx-auto w-full max-w-6xl">
	<Dialog.Root open={showDetails} onOpenChange={() => closeDialog()}>
		<Dialog.Content
			class="h-5/6 w-full max-w-6xl space-y-8 overflow-y-auto rounded-lg p-8 shadow-2xl [&::-webkit-scrollbar]:hidden"
		>
			<div class="mb-8 flex flex-col items-center justify-center">
				<div class="relative">
					<img
						src={displayedAgent.avatar_url}
						alt={displayedAgent.title}
						class="border-primary h-48 w-48 rounded-full border-4 object-cover shadow-2xl"
					/>
					<div
						class="absolute -bottom-2 -right-2 animate-pulse rounded-full bg-blue-500 px-3 py-2 text-xs font-semibold text-white"
					>
						V {displayedAgent.version}
					</div>
				</div>
				<div class="mt-4 flex flex-col items-center">
					{#if displayedAgent.created_at}
						<p class="text-sm text-gray-400">Created {timeSince(displayedAgent.created_at)}</p>
					{/if}
					<div
						class="mt-2 inline-flex items-center justify-center rounded-full bg-green-500 px-3 py-1 text-xs font-semibold text-white shadow"
					>
						Model: {displayedAgent.model}
					</div>
				</div>
			</div>
			<div class="space-y-4 text-center">
				<h2
					class="bg-gradient-to-r from-blue-400 to-teal-300 bg-clip-text py-2 text-6xl font-extrabold text-transparent"
				>
					{displayedAgent.title}
				</h2>
				<p class="mx-auto max-w-3xl text-xl text-gray-400">{displayedAgent.role}</p>
				<!-- <p class="text-lg italic text-gray-500">— {displayedAgent.author}</p> -->
			</div>

			<div class="text-white">
				<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Description</h3>
				<ul class="mt-4 list-inside list-disc space-y-2 text-gray-400">
					{#each displayedAgent.description as description}
						<li>{description}</li>
					{/each}
				</ul>
			</div>

			<div class="mt-6 text-white">
				<h3 class="border-b-2 border-gray-700 pb-2 text-2xl font-semibold">Tools</h3>
				<div class="mt-4 flex flex-wrap gap-2">
					{#each displayedAgent.tools as tool}
						<span
							class="rounded-full bg-gray-700 px-4 py-2 text-sm transition-colors duration-200 hover:bg-gray-600"
							>{tool}</span
						>
					{/each}
				</div>
			</div>
		</Dialog.Content>
	</Dialog.Root>
</div>

