<script lang="ts">
	import {
		SvelteFlow,
		Background,
		Controls,
		Position,
		useEdges,
		ConnectionMode,
		type IsValidConnection,
		getIncomers,
		type Edge,
		type Connection,
		Panel
	} from "@xyflow/svelte";
	import { get, writable } from "svelte/store";
	import ContextMenu from "$lib/components/ContextMenu.svelte";
	import { Button } from "$lib/components/ui/button";
	import * as Dialog from "$lib/components/ui/dialog";

	// 👇 always import the styles
	import "@xyflow/svelte/dist/style.css";
	import RightEditorSidebar from "$lib/components/RightEditorSidebar.svelte";
	import { Library } from "$lib/components/ui/library";

	const nodeDefaults = {
		sourcePosition: Position.Left,
		targetPosition: Position.Right
	};

	const nodes = writable([
		{
			id: "0",
			type: "agent",
			position: { x: 0, y: 0 },
			data: { agent_id: "0" },
			...nodeDefaults
		},
		{
			id: "1",
			type: "agent",
			position: { x: 300, y: 300 },
			data: { agent_id: "1" },

			...nodeDefaults
		},
		{
			id: "2",
			type: "agent",
			position: { x: 500, y: 100 },
			data: { agent_id: "2" },
			...nodeDefaults
		}
	]);
	const edges = writable([
		{
			id: "0-1",
			source: "0",
			target: "1",
			animated: true
		}
	]);

	const nodeTypes = {
		agent: AgentNode
	};

	type Connection = {
		source: string;
		target: string;
		sourceHandle: string | null;
		targetHandle: string | null;
	};

	const onconnect = (connection: Connection) => {
		// Get the source and target from the connection
		let { source, target } = connection;

		// Get the current list of edges
		let currentEdges = $edges;

		// Remove edges between the same two nodes
		let filteredEdges = currentEdges.filter((edge, i) => {
			const isLastNode: boolean = i == currentEdges.length - 1;
			if (
				((edge.source == source && edge.target == target) ||
					(edge.target == source && edge.source == target)) &&
				!isLastNode
			) {
				// Connection between the same nodes already exists
				return false;
			} else {
				return true;
			}
		});

		console.log(
			"filteredEdges",
			filteredEdges,
			"currentEdges",
			currentEdges,
			"source",
			source,
			"target",
			target,
			"connection",
			connection
		);
		// Update the edges store with the filtered list of edges
		edges.set(filteredEdges);
	};

	let menu: { id: string; top?: number; left?: number; right?: number; bottom?: number } | null;
	let width: number;
	let height: number;

	function handleContextMenu({ detail: { event, node } }) {
		// Prevent native context menu from showing
		event.preventDefault();

		// Calculate position of the context menu. We want to make sure it
		// doesn't get positioned off-screen.
		menu = {
			id: node.id,
			top: event.clientY < height - 200 ? event.clientY : undefined,
			left: event.clientX < width - 200 ? event.clientX : undefined,
			right: event.clientX >= width - 200 ? width - event.clientX : undefined,
			bottom: event.clientY >= height - 200 ? height - event.clientY : undefined
		};
	}

	// Close the context menu if it's open whenever the window is clicked.
	function handlePaneClick() {
		menu = null;
	}

	const actions = [
		{ name: "Load Agent" },
		{ name: "Add Prompt" },
		{ name: "Add Model" },
		{ name: "Save" }
	];
</script>

<div class="h-screen w-screen" bind:clientWidth={width} bind:clientHeight={height}>
	<SvelteFlow
		{nodes}
		{edges}
		{nodeTypes}
		onconnectstart={(connection) => console.log("edges: ", $edges, "nodes: ", $nodes)}
		connectionMode={ConnectionMode.Loose}
		snapGrid={[20, 20]}
		connectionRadius={75}
		on:nodecontextmenu={handleContextMenu}
		on:paneclick={handlePaneClick}
		{onconnect}
	>
		<Background class="!bg-background" />
		<Controls />
		{#if menu}
			<ContextMenu
				onClick={handlePaneClick}
				id={menu.id}
				top={menu.top}
				left={menu.left}
				right={menu.right}
				bottom={menu.bottom}
			/>
		{/if}
		<Panel position="top-right">
			<RightEditorSidebar {actions} let:action>
				{#if action.name === "Save"}
					<Button disabled>
						{action.name}
					</Button>
				{:else if ["Load Agent", "Add Modal"].includes(action.name)}
					<Dialog.Root>
						<Dialog.Trigger>
							<Button variant="outline" class="w-full">
								{action.name}
							</Button>
						</Dialog.Trigger>
						<Dialog.Content class="max-w-5xl">
							<Library />
						</Dialog.Content>
					</Dialog.Root>
				{:else}
					<Button variant="outline" class="w-full">
						{action.name}
					</Button>
				{/if}
			</RightEditorSidebar>
		</Panel>
	</SvelteFlow>
</div>
