<script lang="ts">
	import { SvelteFlow, Background, ConnectionLineType, useSvelteFlow } from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';
	import * as Nodes from './nodes';
	import { saveCrew } from '$lib/utils';
	import { setContext, getContext, type CrewContext } from '$lib/context';
	import { writable } from 'svelte/store';
	import CrewPanel from './CrewPanel.svelte';

	export let data;

	let writableData: CrewContext = {
		crew: writable(data.crew),
		nodes: writable(data.nodes)
	};

	setContext('crew', writableData);
	const { crew, nodes } = getContext('crew');

	// update $crew.agents to n.id where it is of type 'agent'
	$: {
		$crew.agents = $nodes.filter((n) => n.type === 'agent').map((n) => n.id);
	}

	// may be able to do some cool localStorage/cookie saving and be more selective
	// about pushing to db and using the api
	let oldCrew = JSON.stringify($crew);
	let lastSaveDate = new Date().getTime();
	$: if (oldCrew !== JSON.stringify($crew) && new Date().getTime() - lastSaveDate > 2000) {
		oldCrew = JSON.stringify($crew);
		lastSaveDate = new Date().getTime();
		(async () => {
			await saveCrew($crew);
		})();
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
				the prompt, and add and remove agents. All agents you add to the crew will be in the same
				crew and will be able to talk with eachother. Don't forget to save!
			</code>
		</div>
	</SvelteFlow>
</div>
