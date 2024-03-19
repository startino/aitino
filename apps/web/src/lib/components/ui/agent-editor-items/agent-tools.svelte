<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { PlusCircle, MinusCircle } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';
	import { createEventDispatcher } from 'svelte';
	import type { Agent } from '$lib/types/models';

	const dispatch = createEventDispatcher();

	export let open = false;
	export let filteredTools;
	export let toolApiKeys;
	export let checkSelected;
	export let displayTools: Agent | null = null;

	let searchQuery = '';

	function handleChange() {
		dispatch('close');
		open = !open;
		console.log(open, 'open 0');
	}

	console.log(open, 'open 1');

	$: filteredTools = displayTools?.toolscolumn?.filter(
		(tool) =>
			tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			tool.description.toLowerCase().includes(searchQuery.toLowerCase())
	);

	$: selectedNewTool = (tool: { name: string; description: string }, apiKey: string) => {
		let newTool = {
			name: tool.name,
			apikey: toolApiKeys[tool.name],
			description: tool.description
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

		<div class="grid grid-cols-3 gap-4">
			{#each filteredTools as tool}
				<form class="relative cursor-pointer rounded-lg p-4 shadow-lg hover:scale-[103%]">
					<Button
						class="bg-ghost"
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
					<div id="tool">
						<h3 class="font-extrabold">{tool?.name}</h3>
						<input type="hidden" name="tool" id="toolsJsonData" value={tool} />
						<p class="text-muted-foreground text-xs">{tool.description}</p>
						<input type="hidden" name="tool" value={tool.name} />

						<div class="mt-3">
							<Input
								type="text"
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
