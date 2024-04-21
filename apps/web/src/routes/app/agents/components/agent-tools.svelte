<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { PlusCircle } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';
	import { createEventDispatcher } from 'svelte';
	import type { Agent } from '$lib/types/models';
	import { enhance } from '$app/forms';

	const dispatch = createEventDispatcher();

	export let open = false;
	let filteredTools: string[];
	export let toolApiKeys: Record<string, string>;
	export let checkSelected: { name: string; apikey: string; description: string; id: string }[];
	export let displayTools: Agent | null = null;
	export let selectedAgent: Agent | null;
	export let agentTools: Agent[] | null;

	$: console.log('agentTools:', agentTools);
	let searchQuery = '';

	$: filteredTools = agentTools.filter(
		(tool) =>
			tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			tool.description.toLowerCase().includes(searchQuery.toLowerCase())
	);

	function handleChange() {
		dispatch('close');
		open = !open;
		console.log(open, 'open 0');
	}

	console.log(open, 'open 1');

	$: selectedNewTool = (
		tool: { name: string; description: string; id: string },
		apiKey: string
	) => {
		let newTool = {
			name: tool.name,
			apikey: toolApiKeys[tool.name],
			description: tool.description,
			id: tool.id
		};
		dispatch('updateCheckSelected', newTool);

		checkSelected = [...checkSelected, newTool];
	};
</script>

<Dialog.Root {open} onOpenChange={handleChange}>
	<Dialog.Content class="mt-8 w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>Search for tools</Dialog.Header>
		<Input
			placeholder="Search tools..."
			type="text"
			bind:value={searchQuery}
			class="focus-visible:ring-1 focus-visible:ring-offset-0"
		/>

		<div class="grid h-96 grid-cols-3 gap-4 overflow-auto [&::-webkit-scrollbar]:hidden">
			{#each filteredTools as tool}
				<form
					class="relative h-full cursor-pointer rounded-lg px-4 shadow-lg hover:scale-[103%]"
					action="?/addTools&id={selectedAgent.id}&toolId={tool.id}"
					method="post"
					use:enhance
				>
					<Button
						type="submit"
						class="bg-ghost absolute right-2 top-0 transform rounded-full p-2 transition-transform duration-300 ease-in-out hover:rotate-90 hover:bg-transparent "
						on:click={() => {
							console.log(tool, toolApiKeys, 'tool api keys');
							if (toolApiKeys[tool.name] === undefined || null || '') {
								toast.error('API key is required');
								return;
							}

							selectedNewTool(tool, toolApiKeys[tool.name]);
							toast.success('Added tool ' + tool.name);
						}}
					>
						<PlusCircle type="submit" class=" transition-colors" />
					</Button>
					<div class="rounded-lg p-8 px-4">
						<h3 class="font-extrabold">{tool?.name}</h3>
						<input type="hidden" name="toolName" id="toolsJsonData" value={tool.name} />
						<p class="text-xs text-muted-foreground">{tool.description}</p>
						<input type="hidden" name="toolDescription" value={tool.description} />
						<input type="hidden" name="toolDescription" value={tool.id} />

						<div class="mt-3">
							<Input
								type="text"
								name="apiKey"
								placeholder="API Key"
								class="focus-visible:ring-1 focus-visible:ring-offset-0"
								bind:value={toolApiKeys[tool.name]}
							/>
						</div>
						{#if toolApiKeys === undefined || null || ''}
							<p class="text-red-500">API key is required</p>
						{/if}
					</div>
				</form>
			{/each}
		</div>
	</Dialog.Content>
</Dialog.Root>
