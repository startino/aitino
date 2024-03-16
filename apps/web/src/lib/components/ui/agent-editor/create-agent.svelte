<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Loader2 } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import { Toggle } from '$lib/components/ui/toggle';
	import { superForm } from 'sveltekit-superforms/client';
	import { createNewAgents, type AgentFormSchema } from '$lib/schema';
	import { type SuperValidated } from 'sveltekit-superforms';
	import { toast } from 'svelte-sonner';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Switch } from '$lib/components/ui/switch';

	export let data: SuperValidated<AgentFormSchema>;

	const { form: formAgent, errors } = superForm(data, {
		validators: createNewAgents
	});

	export let form;

	const dispatch = createEventDispatcher();

	let state: 'loading' | 'error' | 'idle' = 'idle';

	let open = false;
	const handleTrigger = async () => {
		open = true;
	};

	let published = false;
</script>

<Dialog.Root {open} onOpenChange={(o) => dispatch('close')}>
	<div class="absolute bottom-5 right-5">
		<Dialog.Trigger class={buttonVariants({ variant: 'outline' })} on:click={handleTrigger}>
			Create Agent
		</Dialog.Trigger>
	</div>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>
			<Dialog.Title>Create Agent</Dialog.Title>
		</Dialog.Header>
		<form action="?/creatAgents" method="POST" use:enhance>
			<div class="p-6">
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
									<Select.Item value="gpt-3.5-turbo" label="gpt-3.5-turbo"
										>Gpt-3.5-turbo</Select.Item
									>
								</Select.Group>
							</Select.Content>
							<Select.Input name="model" />
						</Select.Root>
					</div>
				</div>
				<Button
					type="submit"
					variant="outline"
					on:click={() => {
						state = 'loading';

						setTimeout(() => {
							if (
								$formAgent.title.length > 0 &&
								$formAgent.role.length > 0 &&
								$formAgent.description.length > 0
							) {
								state = 'idle';

								setTimeout(() => {
									if (form?.message || form.errors) {
										toast.error('Agent could not be created');
									}
								}, 1000);
								open = false;
								toast.success('Agent created successfully');
							} else {
								if ($errors.title || $errors.role || $errors.description) {
									state = 'idle';
								}
							}
						}, 2000);
					}}
					class="flex"
				>
					Create

					{#if state === 'loading'}
						<Loader2 class="ml-2 w-4 animate-spin" />
					{/if}
				</Button>
			</div>
		</form>
	</Dialog.Content>
</Dialog.Root>
