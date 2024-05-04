<script lang="ts">
	import { Panel } from '@xyflow/svelte';
	import { Loader2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import AgentLibrary from './AgentLibrary.svelte';
	import { goto } from '$app/navigation';
	import type { PanelAction } from '$lib/types';
	import { toast } from 'svelte-sonner';
	import { getContext } from '$lib/utils';
	import api from '$lib/api';
	import { PromptEditor } from '$lib/components/ui/prompt-editor';

	let { crew } = getContext('crew');

	let openAgentLibrary = false;

	let panelActions: PanelAction[];
	$: panelActions = [
		{
			name: 'Run',
			buttonVariant: 'default',
			onclick: async () => {
				goto('/app/sessions');
			}
		},
		{
			name: 'Add Agent',
			isCustom: true
		},
		{
			name: 'Export',
			onclick: () => {
				const jsonString = JSON.stringify($crew, null, 2);
				const blob = new Blob([jsonString], { type: 'application/json' });
				const url = window.URL.createObjectURL(blob);
				const a = document.createElement('a');
				a.href = url;
				a.download = 'crew.json';
				document.body.appendChild(a);
				a.click();
				window.URL.revokeObjectURL(url);
				document.body.removeChild(a);
			}
		},
		{
			name: 'Save',
			onclick: async () => {
				toast.message('Saving crew...');

				const response = await api
					.PATCH('/crews/{id}', {
						params: {
							path: {
								id: $crew.id
							}
						},
						body: {
							receiver_id: $crew.receiver_id,
							prompt: $crew.prompt,
							profile_id: $crew.profile_id,
							title: $crew.title,
							published: $crew.published,
							description: $crew.description,
							agents: $crew.agents
						}
					})
					.then(({ data: d, error: e }) => {
						if (e) {
							console.error(`Error saving crew: ${e.detail}`);
							toast.error(
								`Failed to save crew! Please report to dev team with logs from the console.`
							);
							return null;
						}
						if (!d) {
							console.error(`No data returned from agents`);
							toast.error(
								`Failed to save crew! Please report to dev team with logs from the console.`
							);
							return null;
						}
						toast.success('Crew successfully saved!');
						return d;
					});

				return response ? true : false;
			}
		}
	];
</script>

<Panel position="top-right">
	<!-- Static sidebar for desktop -->
	<div
		class="hidden h-full overflow-y-clip rounded-2xl border bg-primary-900/50 p-6 lg:z-50 lg:grid lg:w-72"
	>
		<div class="mb-4 grid">
			<h1 contenteditable on:input={(e) => ($crew.title = e.target.innerText)}>
				{$crew.title}
			</h1>
			<p
				contenteditable
				class="text-sm text-gray-300"
				on:input={(e) => ($crew.description = e.target.innerText)}
			>
				{$crew.description}
			</p>
		</div>
		<!-- Sidebar component, swap this element with another sidebar if you like -->
		<ul role="list" class="grid w-full gap-2">
			{#each panelActions as action}
				<li class="grid">
					{#if action.isCustom}
						<Dialog.Root open={openAgentLibrary} onOpenChange={(o) => (openAgentLibrary = o)}>
							<Dialog.Trigger>
								<Button variant={action.buttonVariant ?? 'outline'} class="w-full">
									{action.name}
								</Button>
							</Dialog.Trigger>
							<Dialog.Content class="max-w-6xl">
								<AgentLibrary />
							</Dialog.Content>
						</Dialog.Root>
					{:else}
						<Button
							on:click={action.onclick}
							variant={action.buttonVariant ?? 'outline'}
							class="w-full"
						>
							<span class="flex gap-2">
								{#if action.loading}
									<Loader2 class="animate-spin" />
								{/if}
								{action.name}
							</span>
						</Button>
					{/if}
				</li>
			{/each}
			<li class="grid">
				<PromptEditor bind:value={$crew.prompt} />
			</li>
		</ul>
	</div>
</Panel>
