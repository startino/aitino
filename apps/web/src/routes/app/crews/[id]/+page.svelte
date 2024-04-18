<script lang="ts">
	import { writable } from 'svelte/store';
	import dagre from '@dagrejs/dagre';
	import {
		SvelteFlow,
		Background,
		Position,
		ConnectionLineType,
		Panel,
		useSvelteFlow,
		type Node,
		type Edge
	} from '@xyflow/svelte';
	import { toast } from 'svelte-sonner';
	import '@xyflow/svelte/dist/style.css';
	import RightEditorSidebar from '$lib/components/RightEditorSidebar.svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { AgentLibrary } from '$lib/components/ui/library';
	import * as CustomNode from '$lib/components/ui/custom-node';
	import { getContext, getCleanNodes } from '$lib/utils';
	import type { PanelAction } from '$lib/types';
	import { AGENT_LIMIT, PROMPT_LIMIT } from '$lib/config';
	import { goto } from '$app/navigation';
	import { setContext } from 'svelte';

	export let data;

	setContext('crew', data);
	let { count, receiver, profileId, crew, agents, publishedAgents, nodes, edges } =
		getContext('crew');

	let openAgentLibrary = false;

	let status: 'saving' | 'running' | 'idle' = 'idle';

	let panelActions: PanelAction[];
	$: panelActions = [
		{
			name: 'Run',
			loading: status === 'running',
			buttonVariant: 'default',
			onclick: async () => {
				const { failed } = await save();
				if (failed) {
					return;
				}
				status = 'running';
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

	const nodeTypes = {
		agent: CustomNode.Agent,
		prompt: CustomNode.Prompt
	};

	const dagreGraph = new dagre.graphlib.Graph();
	dagreGraph.setDefaultEdgeLabel(() => ({}));

	const nodeWidth = 400;
	const nodeHeight = 500;

	const { deleteElements, getNodes, getViewport, setCenter } = useSvelteFlow();

	function getLayoutedElements(nodes: Node[], edges: Edge[], direction = 'TB') {
		const isHorizontal = direction === 'LR';
		dagreGraph.setGraph({ rankdir: direction });

		if (nodes.length > 0) {
			nodes.forEach((node) => {
				dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
			});

			edges.forEach((edge) => {
				dagreGraph.setEdge(edge.source, edge.target);
			});

			dagre.layout(dagreGraph);

			nodes.forEach((node) => {
				const nodeWithPosition = dagreGraph.node(node.id);
				node.targetPosition = isHorizontal ? Position.Left : Position.Top;
				node.sourcePosition = isHorizontal ? Position.Right : Position.Bottom;

				// We are shifting the dagre node position (anchor=center center) to the top left
				// so it matches the React Flow node anchor point (top left).
				node.position = {
					x: nodeWithPosition.x - nodeWidth / 2,
					y: nodeWithPosition.y - nodeHeight / 2
				};
			});
		}

		return { nodes, edges };
	}

	async function save() {
		status = 'saving';

		const response = await (
			await fetch('?/save', {
				method: 'POST',
				body: JSON.stringify(crew)
			})
		).json();

		const result = { failed: response.type === 'error' };

		if (result.failed) {
			toast.error(response.error.message);
		} else {
			toast.success('Crew successfully saved!');
		}

		status = 'idle';
		return result;
	}

	function setReceiver(id: string | null | undefined) {
		if (!id) {
			return;
		}

		const revr = getNodes([id])[0];

		$receiver = { node: revr, targetCount: 1 };
	}

	function layout() {
		const layoutedElements = getLayoutedElements($nodes, $edges);
		$nodes = layoutedElements.nodes;
		$edges = layoutedElements.edges;
	}

	function addAgent(data: any) {
		if ($count.agents >= AGENT_LIMIT) return;

		const existingNode = $nodes.find((node) => node.id === id);
		if (existingNode) {
			console.log(`Node with ID ${id} already exists.`);
			return;
		}

		const position = { ...getViewport() };
		nodes.update((v) => [
			...v,
			{
				id: id,
				type: 'agent',
				position,
				selectable: false,
				data
			}
		]);

		$count.agents++;
	}

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

	layout();
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
	</SvelteFlow>
</div>
