<script lang="ts">
	import { writable, get } from "svelte/store";
	import dagre from "@dagrejs/dagre";
	import {
		SvelteFlow,
		Background,
		Position,
		ConnectionLineType,
		Panel,
		useSvelteFlow,
		type Node,
		type Edge
	} from "@xyflow/svelte";
	import { toast } from "svelte-sonner";

	import "@xyflow/svelte/dist/style.css";

	import RightEditorSidebar from "$lib/components/RightEditorSidebar.svelte";
	import { Button } from "$lib/components/ui/button";
	import * as Dialog from "$lib/components/ui/dialog";
	import { Library } from "$lib/components/ui/library";
	import * as CustomNode from "$lib/components/ui/custom-node";

	import {
		getContext,
		getWritableNodes,
		getCleanNodes,
		pickRandomAvatar,
		pickRandomName,
		getNodesCount
	} from "$lib/utils";
	import type { PanelAction } from "$lib/types";
	import { AGENT_LIMIT, PROMPT_LIMIT } from "$lib/config.js";
	import type { CrewLoad } from "$lib/types/loads";

	export let data: CrewLoad;

	const { receiver, count } = getContext("crew");
	$: data.crew.receiver_id = $receiver ? $receiver.node.id : null;

	let title = data.crew.title;
	$: data.crew.title = title;
	let description = data.crew.description;
	$: data.crew.description = description;

	const actions: PanelAction[] = [
		{
			name: "Run",
			buttonVariant: "default",
			onclick: async () => {
				await save();
				window.location.href = "/app/sessions";
			}
		},
		{ name: "Add Prompt", buttonVariant: "outline", onclick: addNewPrompt },
		{ name: "Add Agent", buttonVariant: "outline", onclick: addNewAgent },
		{ name: "Load Crew", buttonVariant: "outline", isCustom: true },
		{
			name: "Export",
			buttonVariant: "outline",
			onclick: () => {
				const jsonString = JSON.stringify(
					{
						nodes: getCleanNodes($nodes),
						edges: $edges,
						title,
						description,
						receiver_id: $receiver?.node.id ?? null
					},
					null,
					2
				);
				const blob = new Blob([jsonString], { type: "application/json" });
				const url = window.URL.createObjectURL(blob);
				const a = document.createElement("a");
				a.href = url;
				a.download = "crew.json";
				document.body.appendChild(a);
				a.click();
				window.URL.revokeObjectURL(url);
				document.body.removeChild(a);
			}
		},
		{
			name: "Save",
			buttonVariant: "outline",
			onclick: async () => await save()
		},
		{ name: "Layout", buttonVariant: "outline", onclick: layout }
	];

	const nodeTypes = {
		agent: CustomNode.Agent,
		prompt: CustomNode.Prompt
	};

	let libraryOpen = false;

	const dagreGraph = new dagre.graphlib.Graph();
	dagreGraph.setDefaultEdgeLabel(() => ({}));

	const nodeWidth = 400;
	const nodeHeight = 500;

	const { deleteElements, getNodes, getViewport, setCenter } = useSvelteFlow();

	function getLayoutedElements(nodes: Node[], edges: Edge[], direction = "TB") {
		const isHorizontal = direction === "LR";
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

	const nodes = writable<Node[]>(getWritableNodes(data.crew.nodes));
	$: data.crew.nodes = getCleanNodes($nodes);
	const edges = writable<Edge[]>(data.crew.edges);
	$: data.crew.edges = $edges;

	async function save() {
		if (!data.crew.id) {
			data.crew.id = crypto.randomUUID();
		}

		const response = await (
			await fetch("?/save", {
				method: "POST",
				body: JSON.stringify(data.crew)
			})
		).json();

		if (response.error) {
			toast.error(response.error.message);
			return;
		}

		toast.success("Nodes successfully saved!");
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

	function addNewAgent() {
		if ($count.agents >= AGENT_LIMIT) return;

		const position = { ...getViewport() };

		let name = "";

		do {
			name = pickRandomName();
		} while ($nodes.find((n) => n.type === "agent" && get(n.data.name) === name));

		// setCenter(position.x, position.y, { zoom: position.zoom });

		nodes.update((v) => [
			...v,
			{
				id: crypto.randomUUID(),
				type: "agent",
				position,
				selectable: false,
				data: {
					name: writable(name),
					job_title: writable(""),
					prompt: writable(""),
					model: writable({ label: "", value: "" }),
					avatar: pickRandomAvatar()
				}
			}
		]);

		$count.agents++;
	}

	function addNewPrompt() {
		if ($count.prompts >= PROMPT_LIMIT) return;

		const position = { ...getViewport() };
		setCenter(position.x, position.y, { zoom: position.zoom });

		nodes.update((v) => [
			...v,
			{
				id: crypto.randomUUID(),
				type: "prompt",
				selectable: false,
				position,
				data: {
					title: writable(""),
					content: writable("")
				}
			}
		]);

		$count.prompts++;
	}

	console.log(data.crew.id, "from save node 0");
</script>

<div style="height:100vh;">
	<SvelteFlow
		minZoom={0.1}
		{nodes}
		{edges}
		{nodeTypes}
		fitView
		oninit={() => {
			setReceiver(data.crew.receiver_id);
		}}
		connectionLineType={ConnectionLineType.SmoothStep}
		defaultEdgeOptions={{ type: "smoothstep", animated: true }}
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
			if (source.type === "prompt" && target.type === "agent") {
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

			if (source.type === "agent" && target.type === "agent" && $receiver?.node.id === target.id) {
				return;
			}
			return c;
		}}
	>
		<Background class="!bg-background" />

		<Panel position="top-right">
			<RightEditorSidebar bind:description bind:title {actions} let:action>
				{#if action.isCustom}
					<Dialog.Root open={libraryOpen} onOpenChange={(o) => (libraryOpen = o)}>
						<Dialog.Trigger>
							<Button variant={action.buttonVariant} class="w-full">
								{action.name}
							</Button>
						</Dialog.Trigger>
						<Dialog.Content class="max-w-5xl">
							<Library
								on:crew-load={(e) => {
									const crew = e.detail.crew;
									$count = getNodesCount(crew.nodes);
									nodes.set(getWritableNodes(crew.nodes));
									edges.set(crew.edges);
									libraryOpen = false;
									title = crew.title;
									description = crew.description;
									setReceiver(crew.receiver_id);
								}}
							/>
						</Dialog.Content>
					</Dialog.Root>
				{/if}
			</RightEditorSidebar>
		</Panel>
	</SvelteFlow>
</div>
