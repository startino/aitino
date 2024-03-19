<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';
	import type { Agent } from '$lib/types/models';
	import { Button } from '$lib/components/ui/button';
	import { ZodObject, ZodString } from 'zod';
	import { LucidePlusCircle, MinusCircle, PlusCircleIcon } from 'lucide-svelte';
	import AgentTools from './agent-tools.svelte';

	export let selectedAgent: Agent | null = null;
	export let formAgent: SuperFormData<
		ZodObject<{
			title: ZodString;
			role: ZodString;
			description: ZodString;
			published: ZodString;
			model: ZodString;
		}>
	> | null = null;

	export let errors: Record<string, any> | null = null;
	export let isCreate: boolean = false;

	const models = [
		{ value: 'gpt-4-turbo-preview', label: 'gpt-4-turbo-preview' },
		{ value: 'gpt-3.5-turbo', label: 'gpt-3.5-turbo' }
	];

	let toolApiKeys = {} as Record<string, string>;
	let displayTools: Agent | null = null;
	let open = false;
	let searchQuery = '';

	$: published = isCreate ? $formAgent?.published === 'true' : selectedAgent?.published || false;
	$: title = isCreate ? $formAgent?.title : selectedAgent?.title || '';
	$: role = isCreate ? $formAgent?.role : selectedAgent?.role || '';
	$: description = isCreate ? $formAgent?.description : selectedAgent?.description || '';
	$: model = isCreate ? $formAgent?.model : selectedAgent?.model || models[0].value;
	$: prompt = isCreate ? $formAgent?.prompt : selectedAgent?.prompt || '';

	const addTool = ({ currentTool }) => {
		displayTools = currentTool;
	};

	$: filteredTools = displayTools?.toolscolumn?.filter(
		(tool) =>
			tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			tool.description.toLowerCase().includes(searchQuery.toLowerCase())
	);

	$: checkSelected = [] as { name: string; apikey: string; description: string }[];

	const removeSelected = (name: string) => {
		checkSelected = checkSelected.filter((tool) => tool.name !== name);
	}
	const handleClose = () => {
		open = false;
		console.log(open, 'open');
	};
</script>

<div class="p-1">
	<div class="flex w-full items-center gap-2">
		<div class="w-full space-y-4">
			<Label for="title">Title</Label>
			<Input
				id="title"
				name="title"
				value={title}
				on:input={(e) =>
					isCreate ? ($formAgent.title = e.target.value) : (selectedAgent.title = e.target.value)}
				placeholder="Agent's title"
				class="focus-visible:ring-1 focus-visible:ring-offset-0"
			/>
		</div>

		<div class="mt-8 flex items-center space-x-2">
			<Switch
				id="airplane-mode"
				checked={published}
				on:change={(e) =>
					isCreate
						? ($formAgent.published = e.target.checked.toString())
						: (selectedAgent.published = e.target.checked)}
				name="published"
			/>
			<Label for="airplane-mode">Published</Label>
		</div>
	</div>
	{#if isCreate && $errors.title}
		<p class="mb-2 text-red-500">{$errors.title}</p>
	{:else if !isCreate && title === ''}
		<p class="text-red-500">Title is required</p>
	{/if}

	<div class="mt-2 h-52 space-y-2 overflow-auto [&::-webkit-scrollbar]:hidden">
		<Label for="tools">Tools</Label>
		<div class="">
			{#if checkSelected.length > 0}
				<div class="grid grid-cols-3 gap-6 p-6">
					{#each checkSelected as tool}
						<form
							class="shadow-primary relative cursor-pointer rounded-lg p-4 shadow-sm hover:scale-[103%]"
						>
							<Button
								class="bg-card-background hover:bg-card-background"
								on:click={removeSelected(tool.name)}
							>
								<MinusCircle class="text-destructive hover:scale-90" />
							</Button>

							<div
								class="relative flex max-w-sm flex-col rounded-lg p-4 transition-shadow duration-300"
							>
								<div class="text-lg font-semibold">{tool.name}</div>
								<p class="mt-2 text-sm text-gray-500">{tool.description}</p>
							</div>
						</form>
					{/each}
				</div>
			{/if}

			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->

			<div
				class="grid grid-cols-1 gap-4 p-4"
				on:click={() => (
					(open = true),
					console.log(selectedAgent, $formAgent, addTool({ currentTool: selectedAgent }))
				)}
			>
				<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
				<form
					class=" relative flex cursor-pointer
				items-center justify-center rounded-lg p-4 shadow-sm hover:scale-[103%]"
				>
					<PlusCircleIcon
						size="52"
						class="hover:text-primary transition-hover duration-500 hover:scale-95"
					/>
				</form>
				<!-- <form
					class=" relative cursor-pointer rounded-lg
				p-4 shadow-sm hover:scale-[103%]"
				>
					<div class="bg-secondary-100 h-10 w-10 rounded text-center text-black"></div>
					<div id="tool">
						<div class="bg-secondary-100 mt-1 h-4 rounded"></div>
						<div class="bg-secondary-100 mt-1 h-4 w-2/3 rounded"></div>
						<div class="mt-3">
							<div class="bg-secondary-100 h-10 rounded"></div>
						</div>
					</div>
				</form> -->
			</div>
		</div>
	</div>

	<div class="mt-2 space-y-4">
		<div class="flex items-center">
			<span class="text-accent pr-3 font-bold">prompt: </span>
			<Input
				id="prompt"
				name="prompt"
				value={prompt}
				on:input={(e) =>
					isCreate ? ($formAgent.prompt = e.target.value) : (selectedAgent.prompt = e.target.value)}
				placeholder="Add prompt"
				class="border-none focus-visible:ring-1 focus-visible:ring-offset-0"
			/>
		</div>
	</div>

	<div class="mt-2 space-y-2">
		<Label for="role">Role</Label>
		<Input
			id="role"
			name="role"
			value={role}
			on:input={(e) =>
				isCreate ? ($formAgent.role = e.target.value) : (selectedAgent.role = e.target.value)}
			placeholder="Agent's role"
			class="focus-visible:ring-1 focus-visible:ring-offset-0"
		/>
	</div>
	{#if isCreate && $errors.role}
		<p class="mb-2 text-red-500">{$errors.role}</p>
	{:else if !isCreate && role === ''}
		<p class="text-red-500">Role is required</p>
	{/if}

	<div class="mt-2 space-y-2">
		<Label for="description">Description</Label>
		<Textarea
			id="description"
			name="description"
			value={description}
			on:input={(e) =>
				isCreate
					? ($formAgent.description = e.target.value)
					: (selectedAgent.description = e.target.value)}
			placeholder="Describe the agent's purpose"
			class="block h-24 w-full resize-none focus-visible:ring-1 focus-visible:ring-offset-0 [&::-webkit-scrollbar]:hidden"
		></Textarea>
	</div>
	{#if isCreate && $errors.description}
		<p class="mb-2 text-red-500">{$errors.description}</p>
	{:else if !isCreate && description === ''}
		<p class="text-red-500">Description is required</p>
	{/if}

	<div class="mt-2 flex w-full flex-col">
		<Label for="models" class="text-on-background mb-2 font-semibold">Models</Label>
		<Select.Root portal={null} name="model" selected={models.find((m) => m.value === model)}>
			<Select.Trigger class="w-full">
				<Select.Value placeholder="Select a Model" />
			</Select.Trigger>
			<Select.Content>
				<Select.Group>
					<Select.Label>Models</Select.Label>
					{#each models as model}
						<Select.Item value={model.value} label={model.label}>{model.label}</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
			<Select.Input
				name="model"
				value={model}
				on:input={(e) =>
					isCreate ? ($formAgent.model = e.target.value) : (selectedAgent.model = e.target.value)}
			/>
		</Select.Root>
	</div>
</div>

<!-- <Dialog.Root {open} onOpenChange={(o) => (open = false)}>
	<Dialog.Content class="mt-8 w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>Search for tools</Dialog.Header>
		<Input
			placeholder="Search tools..."
			type="text"
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
</Dialog.Root> -->

<AgentTools
	{open}
	on:close={handleClose}
	{toolApiKeys}
	{filteredTools}
	{checkSelected}
	{displayTools}
	on:updateCheckSelected={(event) => {
		checkSelected = [...checkSelected, event.detail];
	}}
/>
