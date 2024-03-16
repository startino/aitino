<script lang="ts">
	import { ComingSoonPage } from '$lib/components/ui/coming-soon';
	import type { Agent } from '$lib/types/models';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Loader2 } from 'lucide-svelte';
	import { applyAction, enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { createEventDispatcher } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { Switch } from '$lib/components/ui/switch';
	import * as Select from '$lib/components/ui/select/index.js';
	import type { ActionData } from '../../../../routes/app/editor/agent/$types';

	export let form: ActionData;

	let state: 'loading' | 'error' | 'idle' = 'idle';

	const dispatch = createEventDispatcher();

	export let selectedAgent: Agent;

	export let open = false;

	const handleChange = () => {
		dispatch('close');
		open = !open;
	};
	$: isFormIncomplete =
		!selectedAgent?.title || !selectedAgent?.role || !selectedAgent?.description;

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
</script>

<Dialog.Root {open} onOpenChange={handleChange}>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>
			<Dialog.Title>Edit Agent</Dialog.Title>
		</Dialog.Header>
		<form
			action="?/editAgent&id=${selectedAgent.id}"
			method="POST"
			use:enhance={() => {
				return async ({ result }) => {
					invalidateAll();
					state = 'idle';
					applyAction(result);
				};
			}}
		>
			<div class="p-6">
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
				{#if selectedAgent.title === ''}
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
				{#if selectedAgent.role === ''}
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
						selected={area[1].value === selectedAgent.model ? area[1] : area[0]}
					>
						<Select.Trigger class="w-full" value={selectedAgent.model}>
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
						<Select.Input name="model" bind:value={selectedAgent.model} />
					</Select.Root>
				</div>
			</div>
			<Button
				type="submit"
				disabled={isFormIncomplete}
				variant="outline"
				class="flex"
				on:click={() => {
					state = 'loading';
					setTimeout(() => {
						if (form?.message) {
							toast.promise(invalidateAll(), {
								loading: 'Editing...',
								success: `${form?.message}`,
								error: 'Error'
							});

							setTimeout(() => {
								state = 'idle';
								open = false;
								location.reload();
							}, 1000);
						}
					}, 2000);
				}}
			>
				Edit

				{#if state === 'loading'}
					<Loader2 class="ml-2 w-4 animate-spin" />
				{/if}
			</Button>
		</form>
	</Dialog.Content>
</Dialog.Root>
