<script lang="ts">
	import { SvelteFlow, Background, ConnectionLineType, useSvelteFlow } from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';
	import * as Nodes from './nodes';
	import { setContext, getContext } from '$lib/utils';
	import type { CrewContext } from '$lib/types/index.js';
	import { writable } from 'svelte/store';
	import CrewPanel from './CrewPanel.svelte';

	export let data;

	let writableData: CrewContext = {
		profileId: writable(data.profileId),
		crew: writable(data.crew),
		agents: writable(data.agents),
		publishedAgents: writable(data.publishedAgents),
		nodes: writable(data.nodes)
	};

	setContext('crew', writableData);
	let { crew, nodes } = getContext('crew');

	const startNodes = $crew.nodes;

	$: $crew.nodes = $nodes.map((n) => n.id);

	const nodeTypes = {
		agent: Nodes.Agent,
		prompt: Nodes.Prompt
	};

	const { getViewport } = useSvelteFlow();
</script>

<div style="height:100vh;">
	<SvelteFlow
		minZoom={0.1}
		{nodes}
		edges={writable([])}
		{nodeTypes}
		fitView
		oninit={() => {
			const position = { ...getViewport() };

			// create prompt
			nodes.update((v) => [
				...v,
				{
					id: crypto.randomUUID(),
					type: 'prompt',
					selectable: false,
					position,
					data: {}
				}
			]);

			// create agents
			for (const agentId of startNodes) {
				nodes.update((v) => [
					...v,
					{
						id: agentId,
						type: 'agent',
						selectable: false,
						position,
						data: {}
					}
				]);
			}
		}}
		connectionLineType={ConnectionLineType.SmoothStep}
		defaultEdgeOptions={{ type: 'smoothstep', animated: true }}
	>
		<Background class="!bg-background" />
		<CrewPanel />
	</SvelteFlow>
</div>
