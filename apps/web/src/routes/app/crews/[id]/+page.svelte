<script lang="ts">
	import { SvelteFlow, Background, ConnectionLineType, useSvelteFlow } from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';
	import * as CustomNode from '$lib/components/ui/custom-node';
	import { setContext, getContext, getCleanNodes } from '$lib/utils';
	import { toast } from 'svelte-sonner';
	import type { CrewContext } from '$lib/types/index.js';
	import { writable } from 'svelte/store';
	import CrewPanel from './CrewPanel.svelte';

	export let data;

	let writableData: CrewContext = {
		count: writable(data.count),
		receiver: writable(data.receiver),
		profileId: writable(data.profileId),
		crew: writable(data.crew),
		agents: writable(data.agents),
		publishedAgents: writable(data.publishedAgents),
		nodes: writable(data.nodes)
	};

	setContext('crew', writableData);
	let { count, receiver, nodes } = getContext('crew');

	const nodeTypes = {
		agent: CustomNode.Agent,
		prompt: CustomNode.Prompt
	};

	const { getNodes } = useSvelteFlow();

	function setReceiver(id: string | null | undefined) {
		if (!id) {
			return;
		}

		const newReceiver = getNodes([id])[0];

		if (!newReceiver) {
			toast.error('Receiver node not found');
			return;
		}

		$receiver = { node: newReceiver, targetCount: 1 };
	}
</script>

<div style="height:100vh;">
	<SvelteFlow
		minZoom={0.1}
		{nodes}
		edges={writable([])}
		{nodeTypes}
		fitView
		oninit={() => {
			setReceiver($receiver ? $receiver.node.id : null);
			getCleanNodes($nodes).forEach((n) => {
				if (n.type === 'agent') {
					$count.agents++;
				} else {
					$count.prompts++;
				}
			});
		}}
		connectionLineType={ConnectionLineType.SmoothStep}
		defaultEdgeOptions={{ type: 'smoothstep', animated: true }}
	>
		<Background class="!bg-background" />
		<CrewPanel />
	</SvelteFlow>
</div>
