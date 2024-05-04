<script lang="ts">
	import { SvelteFlow, Background, ConnectionLineType, useSvelteFlow } from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';
	import * as Nodes from './nodes';
	import { setContext, getContext } from '$lib/utils';
	import type { CrewContext } from '$lib/types';
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

	// update $crew.agents to n.id where it is of type 'agent'
	$: {
		console.log('Updating agents');
		$crew.agents = $nodes.filter((n) => n.type === 'agent').map((n) => n.id);
		console.log($crew.agents);
	}

	const nodeTypes = {
		agent: Nodes.Agent
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

			// create agents
			console.log(`adding startNodes: ${data.startNodes}`);
			for (const agentId of data.startNodes) {
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
		<div class="absolute bottom-0 flex w-full items-center justify-center p-4 text-center">
			<code class="text-red-400">
				Currently the node editor is only capable of the bare essentials. That means you can edit
				the prompt, and add and remove agents.
			</code>
		</div>
	</SvelteFlow>
</div>
