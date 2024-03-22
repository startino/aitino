<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';
	import type { Agent } from '$lib/types/models';
	import { Button } from '$lib/components/ui/button';
	import { ZodObject, ZodString } from 'zod';
	import { MinusCircle, PlusIcon } from 'lucide-svelte';
	import { AgentTools } from '$lib/components/ui/agent-editor-items/';
	import { enhance } from '$app/forms';

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

	{#if !isCreate}
		<div class="mt-2 h-52 space-y-2 overflow-auto [&::-webkit-scrollbar]:hidden">
			<Label for="tools">Tools</Label>
			<div>
				<div class="grid grid-cols-3 gap-6 px-6">
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
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
		</div>{/if}

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
