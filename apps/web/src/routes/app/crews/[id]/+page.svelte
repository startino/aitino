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
		nodes: writable(data.nodes),
		edges: writable(data.edges)
	};

	setContext('crew', writableData);
	let { count, receiver, nodes, edges } = getContext('crew');

	const nodeTypes = {
		agent: CustomNode.Agent,
		prompt: CustomNode.Prompt
	};

	const { deleteElements, getNodes } = useSvelteFlow();

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
		{edges}
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
		on:edgeclick={(e) => {
			const edge = e.detail.edge;
			deleteElements({ edges: [{ id: edge.id }] });

			if ($receiver && edge.target === $receiver.node.id) {
				$receiver.targetCount--;
				$receiver.targetCount === 0 && ($receiver = null);
			}
		}}
		onedgecreate={(c) => {
			const [source, target] = getNodes([c.source, c.target]);
			if (!source) {
				toast.error('Source node not found');
				return;
			}
			if (!target) {
				toast.error('Target node not found');
				return;
			}

			if (source.type === 'prompt' && target.type === 'agent') {
				if ($receiver) {
					if (target.id !== $receiver.node.id) {
						return;
					} else {
						$receiver.targetCount++;
					}
				} else {
					$receiver = { node: target, targetCount: 1 };
				}
			}

			if (source.type === 'agent' && target.type === 'agent' && $receiver?.node.id === target.id) {
				return;
			}
			return c;
		}}
	>
		<Background class="!bg-background" />
		<CrewPanel />
	</SvelteFlow>
</div>
