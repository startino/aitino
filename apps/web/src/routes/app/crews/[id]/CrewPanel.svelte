<script lang="ts">
	import { Panel, useSvelteFlow } from '@xyflow/svelte';
	import { X, Loader2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import AgentLibrary from './AgentLibrary.svelte';
	import { goto } from '$app/navigation';
	import type { PanelAction } from '$lib/types';
	import { AGENT_LIMIT } from '$lib/config';
	import { toast } from 'svelte-sonner';
	import { getContext, getCleanNodes } from '$lib/utils';
	import api from '$lib/api';

	let { receiver, crew, agents, publishedAgents, nodes } = getContext('crew');

	let openAgentLibrary = false;

	async function save() {
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
					published: $crew.published,
					title: $crew.title,
					description: $crew.description,
					edges: [],
					nodes: $agents.map((n: any) => n.id)
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error saving crew: ${e.detail}`);
					toast.error(`Failed to save crew! Please report to dev team with logs from the console.`);
					return null;
				}
				if (!d) {
					console.error(`No data returned from agents`);
					toast.error(`Failed to save crew! Please report to dev team with logs from the console.`);
					return null;
				}
				toast.success('Crew successfully saved!');
				return d;
			});

		return response ? true : false;
	}

	const { getViewport } = useSvelteFlow();

	function addAgent(data: any) {
		if ($agents.length >= AGENT_LIMIT) return;

		const existingNode = $nodes.find((node) => node.id === data.id);
		if (existingNode) {
			console.log(`Node with ID ${data.id} already exists.`);
			return;
		}

		const position = { ...getViewport() };
		nodes.update((v) => [
			...v,
			{
				id: data.id,
				type: 'agent',
				position,
				selectable: false,
				data
			}
		]);
	}

	let panelActions: PanelAction[];
	$: panelActions = [
		{
			name: 'Run',
			buttonVariant: 'default',
			onclick: async () => {
				goto('/app/session');
			}
		},
		{
			name: 'Add Agent',
			isCustom: true
		},
		{
			name: 'Export',
			onclick: () => {
				const jsonString = JSON.stringify(
					{
						nodes: getCleanNodes($nodes),
						title: $crew.title,
						description: $crew.description,
						receiver_id: $receiver?.node.id ?? null
					},
					null,
					2
				);
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
			onclick: save
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
								<AgentLibrary
									agents={$agents}
									publishedAgents={$publishedAgents}
									on:load-agent={({ detail }) => {
										addAgent(detail);
									}}
								/>
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
		</ul>
	</div>
</Panel>
