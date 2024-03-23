<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';
	import type { Agent } from '$lib/types/models';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { ZodObject, ZodString, string } from 'zod';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { Plus, ChevronDown } from 'lucide-svelte';
	import { AgentTools } from '$lib/components/ui/agent-editor-items/';
	import { slide } from 'svelte/transition';
	import { toast } from 'svelte-sonner';

	type AgentTools = {
		id: string;
		name: string;
		description: string;
		api_key_types_id: string;
		created_at: string;
	};

	export let apiKeyTypes: ArrayLike<unknown> | Iterable<unknown>;
	export let agentTools: AgentTools[];
	export let selectedAgent: Agent;
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

	let toolApiKeys = {} as Record<string, string>;
	let open = false;

	const models = [
		{ value: 'gpt-4-turbo-preview', label: 'gpt-4-turbo-preview' },
		{ value: 'gpt-3.5-turbo', label: 'gpt-3.5-turbo' }
	];

	$: published = isCreate ? $formAgent?.published === 'true' : selectedAgent?.published || false;
	$: title = isCreate ? $formAgent?.title : selectedAgent?.title || '';
	$: role = isCreate ? $formAgent?.role : selectedAgent?.role || '';
	$: description = isCreate ? $formAgent?.description : selectedAgent?.description || '';
	$: model = isCreate ? $formAgent?.model : selectedAgent?.model || models[0].value;
	$: system_message = isCreate ? $formAgent?.system_message : selectedAgent?.system_message || '';

	$: checkSelected = [] as { name: string; apikey: string; description: string; id: string }[];

	const handleClose = () => {
		open = false;
		console.log(open, 'open');
	};

	$: {
		if (agentTools && selectedAgent?.tools) {
			checkSelected = agentTools
				.filter((tool) => selectedAgent?.tools.some((selectedTool) => selectedTool.id === tool.id))
				.map((tool) => ({
					id: tool.id,
					name: tool.name,
					apikey: tool.apikey,
					description: tool.description
				}));
		}
	}

	let filter_tools_based_on_agent = agentTools
		.filter((tool) => selectedAgent?.tools.some((selectedTool) => selectedTool.id === tool.id))
		.map((tool) => ({
			id: tool.id,
			name: tool.name,
			api_key_types_id: tool.api_key_types_id,
			description: tool.description
		}));

	console.log(filter_tools_based_on_agent, 'filter tools based on agent');

	let showToolsDetail = false;

	let addedTools = [] as {
		id: string;
		name: string;
		api_key_types_id: string;
		description: string;
	}[];

	addedTools = [...addedTools, ...filter_tools_based_on_agent];

	$: searchQuery = '';
	$: filted_from_search = agentTools.filter(
		(tool) =>
			tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
			tool.description.toLowerCase().includes(searchQuery.toLowerCase())
	);

	$: console.log(agentTools, 'searchQuery', filted_from_search, 'filted_from_search');

	let selectedName: string;
	let selectedId: string;

	function handleSelect(tool: {
		id: string;
		name: string;
		api_key_types_id: string;
		description: string;
	}) {
		selectedName = tool.name;
		selectedId = tool.id;
		console.log(selectedName, 'new api name here');
	}
</script>

<div class="p-1">
	<div class="mb-2 flex w-full items-center gap-2">
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

	<span class="mt-4 pr-3 font-bold">Tools: </span>
	<div class="grid h-48 grid-cols-3 gap-4 overflow-auto [&::-webkit-scrollbar]:hidden">
		<!-- svelte-ignore missing-declaration -->
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		{#if !showToolsDetail}
			<div
				class="from-primary-900 to-primary-950 mt-2 flex cursor-pointer items-center justify-center space-y-4 rounded-lg bg-gradient-to-t p-4 text-center text-white transition-all duration-500"
				transition:slide={{ duration: 400 }}
				on:click={() => {
					showToolsDetail = true;
				}}
			>
				<div class="flex items-center justify-center transition-all duration-500">
					<h3 class="font-extrabold"><Plus /></h3>
				</div>
			</div>

			{#if addedTools.length > 0}
				{#each addedTools as tool}
					<div
						class="from-primary-800 to-primary-950 mt-2 cursor-pointer space-y-4 rounded-lg bg-gradient-to-t p-4 text-center text-current transition-all duration-500"
						transition:slide={{ duration: 400 }}
					>
						<div
							class="flex flex-col items-center justify-center"
							transition:slide={{ duration: 400 }}
						>
							<h3 class="font-extrabold">{tool.name}</h3>
							{#if isCreate}
								<input type="hidden" name="id" id="toolsJsonData" bind:value={$formAgent.id} />
							{:else}
								<input type="hidden" name="id" id="toolsJsonData" bind:value={selectedAgent.id} />
							{/if}
							<p class="text-muted-foreground text-xs">{tool.description}</p>
						</div>
					</div>{/each}
			{/if}
		{/if}
		{#if showToolsDetail}
			<Dialog.Root open={showToolsDetail} onOpenChange={() => (showToolsDetail = false)}>
				<Dialog.Content class="w-full max-w-4xl">
					<Dialog.Header>Search for tools</Dialog.Header>
					<Input
						placeholder="Search tools..."
						type="text"
						bind:value={searchQuery}
						class="focus-visible:ring-1 focus-visible:ring-offset-0"
					/>

					{#if filted_from_search.length === 0}
						<div class="flex h-full w-full items-center justify-center">
							<h3 class="">No tools found!</h3>
						</div>
					{/if}
					<div class="grid h-96 grid-cols-3 gap-4 overflow-auto [&::-webkit-scrollbar]:hidden">
						{#each filted_from_search as tool}
							<div
								class="from-primary-900 to-primary-950 relative mt-2 cursor-pointer space-y-4 rounded-lg bg-gradient-to-t p-4 text-center text-white transition-all duration-500"
								transition:slide={{ duration: 400 }}
							>
								<div class="flex flex-col items-center justify-between">
									<h3 class="font-extrabold">{tool.name}</h3>
									{#if isCreate}
										<input type="hidden" name="id" id="toolId" bind:value={$formAgent.id} />
									{:else}
										<input type="hidden" name="id" id="toolId" bind:value={selectedAgent.id} />
									{/if}
									<p class="text-muted-foreground text-xs">{tool.description}</p>
								</div>

								<!-- svelte-ignore a11y-click-events-have-key-events -->
								<!-- svelte-ignore a11y-no-static-element-interactions -->
								<div
									on:click|stopPropagation={() => (
										(showToolsDetail = true), console.log(apiKeyTypes, 'from click')
									)}
									class="w-full"
								>
									<DropdownMenu.Root>
										<DropdownMenu.Trigger asChild let:builder>
											<Button variant="outline" class="ml-auto w-full" builders={[builder]}>
												Select your API <ChevronDown class="ml-2 h-4 w-4" />
											</Button>
										</DropdownMenu.Trigger>
										<DropdownMenu.Content class="z-50">
											{#each apiKeyTypes as api}
												<DropdownMenu.CheckboxItem
													checked={selectedName === api.name}
													on:click={() => handleSelect(api)}
												>
													{api.name}
												</DropdownMenu.CheckboxItem>
											{/each}
										</DropdownMenu.Content>
									</DropdownMenu.Root>
								</div>
								<div class="text-background relative my-4 p-6">
									<Button
										class="absolute bottom-0 left-0 flex w-full items-center justify-center"
										on:click={() => {
											if (selectedId === tool.api_key_types_id) {
												console.log(selectedId, 'from success selected id here');

												showToolsDetail = false;
												addedTools = [...addedTools, tool];
											} else {
												console.log(selectedId, 'failure selected id here');
												console.log(tool.api_key_types_id, 'apik selected id here');
												showToolsDetail = true;
												toast.error('Please select correct API key type');
											}
											if (isCreate) {
												$formAgent.id = tool.id;
											} else {
												selectedAgent.id = tool.id;
											}
										}}
									>
										<Plus /> Add tool</Button
									>
								</div>
							</div>
						{/each}
					</div>
				</Dialog.Content>
			</Dialog.Root>
		{/if}
	</div>

	<div class="mt-2 space-y-4">
		<div class="flex items-center">
			<span class="text-accent pr-3 font-bold">prompt: </span>
			<Input
				id="prompt"
				name="prompt"
				value={system_message}
				on:input={(e) =>
					isCreate
						? ($formAgent.system_message = e.target.value)
						: (selectedAgent.system_message = e.target.value)}
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

<AgentTools
	{open}
	on:close={handleClose}
	{toolApiKeys}
	{checkSelected}
	on:updateCheckSelected={(event) => {
		checkSelected = [...checkSelected, event.detail];
	}}
	{selectedAgent}
	{agentTools}
/>
