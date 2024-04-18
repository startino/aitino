<script lang="ts">
	import { Panel, useSvelteFlow } from '@xyflow/svelte';
	import RightEditorSidebar from '$lib/components/RightEditorSidebar.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { AgentLibrary } from '$lib/components/ui/library';
	import { goto } from '$app/navigation';
	import { getContext } from '$lib/utils';
	import type { PanelAction } from '$lib/types';
	import { PROMPT_LIMIT } from '$lib/config';
	import { writable } from 'svelte/store';
	import { toast } from 'svelte-sonner';
	import api from '$lib/api';
	import { error } from '@sveltejs/kit';

	let { count, receiver, profileId, crew, agents, publishedAgents, nodes, edges } =
		getContext('crew');

	async function save() {
		toast.message('Saving crew...');

		const response = await api
			.PATCH('/crews/{crew_id}', {
				params: {
					path: {
						crew_id: $crew.id
					}
				},
				body: {
					receiver_id: $crew.receiver_id,
					prompt: $crew.prompt,
					profile_id: $crew.profile_id,
					published: $crew.published,
					title: $crew.title,
					description: $crew.description,
					edges: $crew.edges,
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

	const { deleteElements, getNodes, getViewport, setCenter } = useSvelteFlow();
	function addPrompt() {
		if ($count.prompts >= PROMPT_LIMIT) return;

		const position = { ...getViewport() };
		setCenter(position.x, position.y, { zoom: position.zoom });

		nodes.update((v) => [
			...v,
			{
				id: crypto.randomUUID(),
				type: 'prompt',
				selectable: false,
				position,
				data: {
					title: writable(''),
					content: writable('')
				}
			}
		]);

		$count.prompts++;
	}

	let panelActions: PanelAction[];
	$: panelActions = [
		{
			name: 'Run',
			loading: status === 'running',
			buttonVariant: 'default',
			onclick: async () => {
				goto('/app/session');
			}
		},
		{ name: 'Add Prompt', buttonVariant: 'outline', onclick: addPrompt },
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
						edges: $edges,
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
			loading: status === 'saving',
			onclick: save
		},
		{ name: 'Layout', onclick: layout }
	];
</script>

<Panel position="top-right">
	<RightEditorSidebar
		bind:description={$crew.description}
		bind:title={$crew.title}
		actions={panelActions}
		let:action
	>
		{#if action.isCustom}
			<Dialog.Root open={openAgentLibrary} onOpenChange={(o) => (openAgentLibrary = o)}>
				<Dialog.Trigger>
					<Button variant={action.buttonVariant ?? 'outline'} class="w-full">
						{action.name}
					</Button>
				</Dialog.Trigger>
				<Dialog.Content class="max-w-6xl">
					<AgentLibrary
						myAgents={agents}
						{publishedAgents}
						on:load-agent={({ detail }) => {
							addAgent(detail);
						}}
					/>
				</Dialog.Content>
			</Dialog.Root>
		{/if}
	</RightEditorSidebar>
</Panel>
