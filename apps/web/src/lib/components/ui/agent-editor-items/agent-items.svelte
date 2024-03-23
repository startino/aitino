<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';
	import type { Agent } from '$lib/types/models';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { ZodObject, ZodString } from 'zod';
	import { MinusCircle, PlusIcon, Plus } from 'lucide-svelte';
	import { AgentTools } from '$lib/components/ui/agent-editor-items/';
	import { enhance } from '$app/forms';
	import { slide } from 'svelte/transition';

	export let agentTools: Agent[] | null;
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
	let toolApiKeys = {} as Record<string, string>;
	let displayTools: Agent | null = null;
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

	const addTool = ({ currentTool }) => {
		checkSelected = [...checkSelected, currentTool];
	};

	$: checkSelected = [] as { name: string; apikey: string; description: string; id: string }[];

	const removeSelected = (name: string) => {
		checkSelected = checkSelected.filter((tool) => tool.name !== name);
	};
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
			apikey: tool.apikey,
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

	$: console.log(searchQuery, 'searchQuery', filted_from_search, 'filted_from_search');
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

	<!-- main tools style here  -->
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
							<!-- svelte-ignore a11y-click-events-have-key-events -->
							<!-- svelte-ignore a11y-no-static-element-interactions -->
							<div
								class="from-primary-900 to-primary-950 relative z-50 mt-2 cursor-pointer space-y-4 rounded-lg bg-gradient-to-t p-4 text-center text-white transition-all duration-500"
								transition:slide={{ duration: 400 }}
								on:click={() => {
									if (isCreate) {
										$formAgent.id = tool.id;
									} else {
										selectedAgent.id = tool.id;
									}
									showToolsDetail = false;
									addedTools = [...addedTools, tool];
									addedTools.map((tool) => {
										console.log([tool.id], 'tool id here');
									});
									console.log(addedTools, 'add tools here');
								}}
							>
								<Plus
									class="text-primary-900 absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] opacity-0 hover:-z-50 hover:opacity-100"
									size="100"
								/>

								<div class="flex flex-col items-center justify-center">
									<h3 class="font-extrabold">{tool.name}</h3>
									{#if isCreate}
										<input type="hidden" name="id" id="toolId" bind:value={$formAgent.id} />
									{:else}
										<input type="hidden" name="id" id="toolId" bind:value={selectedAgent.id} />
									{/if}
									<p class="text-muted-foreground text-xs">{tool.description}</p>
								</div>
							</div>
						{/each}
					</div>
				</Dialog.Content>
			</Dialog.Root>
			<!-- {#each agentTools as tool} -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->

			<!-- <div
					class="from-primary-900 to-primary-800 relative z-50 mt-2 cursor-pointer space-y-4 rounded-lg bg-gradient-to-t p-4 text-center text-white transition-all duration-500"
					transition:slide={{ duration: 400 }}
					on:click={() => {
						if (isCreate) {
							$formAgent.id = tool.id;
						} else {
							selectedAgent.id = tool.id;
						}
						showToolsDetail = false;
						addedTools = [...addedTools, tool];
						addedTools.map((tool) => {
							console.log([tool.id], 'tool id here');
						});
						console.log(addedTools, 'add tools here');
					}}
				>
					<Plus
						class="text-primary-900 absolute left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] opacity-0 hover:-z-50 hover:opacity-100"
						size="100"
					/>

					<div class="flex flex-col items-center justify-center">
						<h3 class="font-extrabold">{tool.name}</h3>
						{#if isCreate}
							<input type="hidden" name="id" id="toolId" bind:value={$formAgent.id} />
						{:else}
							<input type="hidden" name="id" id="toolId" bind:value={selectedAgent.id} />
						{/if}
						<p class="text-muted-foreground text-xs">{tool.description}</p>
					</div>
				</div> -->
			<!-- {/each} -->
		{/if}
	</div>

	<!-- {#if !isCreate}
		<div class="mt-2 h-52 space-y-2 overflow-auto [&::-webkit-scrollbar]:hidden">
			<Label for="tools">Tools</Label>
			<div>
				<div class="grid grid-cols-3 gap-6 px-6">
					<div
						class="border-nprimary relative flex h-full cursor-pointer justify-center gap-4 rounded-lg border px-4 shadow-sm transition duration-300 ease-in-out"
						on:click={() => (
							(open = true),
							console.log(selectedAgent, $formAgent, addTool({ currentTool: selectedAgent }))
						)}
					>
						<form
							class="relative flex cursor-pointer items-center justify-center rounded-lg p-4 shadow-sm"
						>
							<PlusIcon
								size="52"
								class="bg-nprimary text-nprimary-on hover:bg-nprimary-container hover:text-nprimary-container-on flex items-center justify-center gap-2 rounded-full p-2 transition-colors duration-300 ease-in-out"
							/>
						</form>
					</div>

					{#if checkSelected.length > 0}
						{#each checkSelected as tool}
							<form
								action="?/removeTools&id={selectedAgent.id}&toolId={tool.id}"
								method="POST"
								use:enhance
								class=" border-nprimary bg-surface hover:border-nprimary group overflow-hidden rounded-lg border transition duration-300 ease-in-out"
							>
								<div
									class=" relative p-4 shadow-sm transition-shadow duration-300 ease-in-out hover:shadow-lg"
								>
									<h3 class="text-primary-500 pr-4 text-xl font-bold">{tool.name}</h3>
									<p class="text-secondary-100">{tool.description}</p>
									<Button
										type="submit"
										class="absolute right-2 top-2 transform rounded-full bg-transparent p-2 transition-transform duration-300 ease-in-out hover:rotate-90 hover:bg-transparent "
										on:click={() => {
											setTimeout(() => {
												removeSelected(tool.name);
											}, 3000);
										}}
									>
										<MinusCircle class="text-destructive h-5 w-5" />
									</Button>
								</div>
							</form>
						{/each}
					{/if}
				</div>
			</div>
		</div>{/if} -->

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
