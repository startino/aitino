<!-- <script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';
	import type { Agent } from '$lib/types/models';
	import { ZodObject, ZodString } from 'zod';

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

	const area = [
		{
			value: 'gpt-4-turbo-preview',
			label: 'gpt-4-turbo-preview'
		},
		{
			value: 'gpt-3.5-turbo',
			label: 'gpt-3.5-turbo'
		}
	];

	let published = false;
</script>

<div class="p-6">
	{#if isCreate}
		<div class="flex w-full items-center gap-4">
			<div class="mb-4 w-full space-y-4">
				<Label for="title" class="block text-sm font-medium ">Title</Label>
				<Input
					id="title"
					name="title"
					bind:value={$formAgent.title}
					placeholder="Agent's title"
					class="focus-visible:ring-1 focus-visible:ring-offset-0"
				/>
			</div>

			<div class="mt-4 flex items-center space-x-2">
				<Switch id="airplane-mode" bind:checked={published} name="published" />
				<Label for="airplane-mode">Published</Label>
			</div>
		</div>
		{#if $errors.title}
			<p class="mb-2 text-red-500">{$errors.title}</p>
		{/if}
		<div class="mb-4 space-y-4">
			<Label for="role" class="block text-sm font-medium ">Role</Label>
			<Input
				id="role"
				name="role"
				bind:value={$formAgent.role}
				placeholder="Agent's role"
				class="focus-visible:ring-1 focus-visible:ring-offset-0"
			/>
		</div>
		{#if $errors.role}
			<p class="mb-2 text-red-500">{$errors.role}</p>
		{/if}
		<div class="mb-4 space-y-4">
			<Label for="description" class="block text-sm font-medium ">Description</Label>
			<Textarea
				id="description"
				name="description"
				bind:value={$formAgent.description}
				placeholder="Describe the agent's purpose"
				class="block h-24 w-full resize-none focus-visible:ring-1 focus-visible:ring-offset-0 [&::-webkit-scrollbar]:hidden"
			></Textarea>
		</div>
		{#if $errors.description}
			<p class="mb-2 text-red-500">{$errors.description}</p>
		{/if}
		<div class="flex w-full gap-4">
			<div class="mb-4 flex w-full flex-col">
				<Label for="models" class="text-on-background mb-2 font-semibold">Models</Label>
				<Select.Root portal={null} name="model">
					<Select.Trigger class="w-full">
						<Select.Value placeholder="Select a Model" />
					</Select.Trigger>
					<Select.Content>
						<Select.Group>
							<Select.Label>Models</Select.Label>
							<Select.Item value="gpt-4-turbo-preview" label="gpt-4-turbo-preview"
								>Gpt-4</Select.Item
							>
							<Select.Item value="gpt-3.5-turbo" label="gpt-3.5-turbo">Gpt-3.5-turbo</Select.Item>
						</Select.Group>
					</Select.Content>
					<Select.Input name="model" />
				</Select.Root>
			</div>
		</div>
	{:else}
		<div class="flex w-full items-center gap-4">
			<div class="mb-4 w-full space-y-4">
				<Label for="title" class="block text-sm font-medium ">Title</Label>
				<Input
					id="title"
					name="title"
					bind:value={selectedAgent.title}
					placeholder="Agent's title"
					class="focus-visible:ring-1 focus-visible:ring-offset-0"
				/>
			</div>

			<div class="mt-4 flex items-center space-x-2">
				<Switch id="airplane-mode" bind:checked={selectedAgent.published} name="published" />
				<Label for="airplane-mode">Published</Label>
			</div>
		</div>
		{#if selectedAgent?.title === ''}
			<p class="text-red-500">Title is required</p>
		{/if}
		<div class="mb-4 space-y-4">
			<Label for="role" class="block text-sm font-medium ">Role</Label>
			<Input
				id="role"
				name="role"
				placeholder="Agent's role"
				bind:value={selectedAgent.role}
				class="focus-visible:ring-1 focus-visible:ring-offset-0"
			/>
		</div>
		{#if selectedAgent?.role === ''}
			<p class="text-red-500">Role is required</p>
		{/if}
		<div class="mb-4 space-y-4">
			<Label for="description" class="block text-sm font-medium ">Description</Label>
			<Textarea
				id="description"
				name="description"
				bind:value={selectedAgent.description}
				placeholder="Describe the agent's purpose"
				class="block h-24 w-full resize-none focus-visible:ring-1 focus-visible:ring-offset-0 [&::-webkit-scrollbar]:hidden"
			></Textarea>
		</div>
		{#if selectedAgent.description === ''}
			<p class="text-red-500">Description is required</p>
		{/if}
		<div class="flex w-full flex-col">
			<Label for="models" class="text-on-background mb-2 font-semibold">Models</Label>
			<Select.Root
				portal={null}
				name="model"
				selected={area[1].value === selectedAgent?.model ? area[1] : area[0]}
			>
				<Select.Trigger class="w-full" value={selectedAgent?.model}>
					<Select.Value placeholder="Select a Model" />
				</Select.Trigger>
				<Select.Content>
					<Select.Group>
						<Select.Label>Models</Select.Label>
						<Select.Item value="gpt-4-turbo-preview" label="gpt-4-turbo-preview">Gpt-4</Select.Item>
						<Select.Item value="gpt-3.5-turbo" label="gpt-3.5-turbo">Gpt-3.5-turbo</Select.Item>
					</Select.Group>
				</Select.Content>
				<Select.Input name="model" bind:value={selectedAgent.model} />
			</Select.Root>
		</div>{/if}
</div> -->

<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';
	import type { Agent } from '$lib/types/models';
	import { ZodObject, ZodString } from 'zod';

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

	$: published = isCreate ? $formAgent?.published === 'true' : selectedAgent?.published || false;
	$: title = isCreate ? $formAgent?.title : selectedAgent?.title || '';
	$: role = isCreate ? $formAgent?.role : selectedAgent?.role || '';
	$: description = isCreate ? $formAgent?.description : selectedAgent?.description || '';
	$: model = isCreate ? $formAgent?.model : selectedAgent?.model || models[0].value;
</script>

<div class="p-6">
	<div class="flex w-full items-center gap-4">
		<div class="mb-4 w-full space-y-4">
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

		<div class="mt-4 flex items-center space-x-2">
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

	<div class="mb-4 space-y-4">
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

	<div class="mb-4 space-y-4">
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

	<div class="flex w-full flex-col">
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
