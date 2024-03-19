<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';
	import type { Agent } from '$lib/types/models';
	import { Button } from '$lib/components/ui/button';
	import { ZodObject, ZodString } from 'zod';
	import { PlusCircle } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';

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

	const tools = [
		{
			name: 'python tools',
			description: 'this tool will help you to write python code faster and easier'
		},
		{
			name: 'uber',
			description: ' this tools is used to generate location data from google maps api'
		},
		{
			name: 'healthyfy',
			description: 'healthfy is used to generate health data from public health data sources'
		},
		{
			name: 'notebook',
			description: 'this tool will help you to save money on your car loan, flight ticket, and more'
		}
	];

	$: selectedTools = [] as { name: string; apiKey: string; description: string }[];

	let toolApiKeys = {} as Record<string, string>;

	$: console.log(selectedTools, 'selectedTools');
	$: published = isCreate ? $formAgent?.published === 'true' : selectedAgent?.published || false;
	$: title = isCreate ? $formAgent?.title : selectedAgent?.title || '';
	$: role = isCreate ? $formAgent?.role : selectedAgent?.role || '';
	$: description = isCreate ? $formAgent?.description : selectedAgent?.description || '';
	$: model = isCreate ? $formAgent?.model : selectedAgent?.model || models[0].value;
	$: prompt = isCreate ? $formAgent?.prompt : selectedAgent?.prompt || '';
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
		<div class="grid grid-cols-3 gap-4">
			{#each tools as tool}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
				<form class="relative cursor-pointer rounded-lg p-4 shadow-lg hover:scale-[103%]">
					<Button
						class="bg-ghost"
						on:click={() => {
							console.log(tool, toolApiKeys, 'tool api keys');
							if (toolApiKeys[tool.name] === undefined || null || '') {
								toast.error('API key is required');
								return;
							}
							selectedTools.push({
								name: tool.name,
								apiKey: toolApiKeys[tool.name],
								description: tool.description
							});
							toast.success('Added tool ' + tool.name);
							console.log(selectedTools, 'selected tools');
						}}
					>
						<PlusCircle type="submit" class=" transition-colors" /></Button
					>
					<div id="tool">
						<h3 class="font-extrabold">{tool.name}</h3>
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
	</div>

	<div class="mt-2 space-y-4">
		<Label for="model">Prompt</Label>
		<Input
			id="prompt"
			name="prompt"
			value={prompt}
			on:input={(e) =>
				isCreate ? ($formAgent.prompt = e.target.value) : (selectedAgent.prompt = e.target.value)}
			placeholder="Add prompt"
			class="focus-visible:ring-1 focus-visible:ring-offset-0"
		/>
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
