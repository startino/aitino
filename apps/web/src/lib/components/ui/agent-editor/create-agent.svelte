<script lang="ts">
	import { applyAction, enhance } from '$app/forms';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Loader2 } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import { Toggle } from '$lib/components/ui/toggle';
	import { invalidateAll } from '$app/navigation';
	import { superForm } from 'sveltekit-superforms/client';

	import * as Form from '$lib/components/ui/form';
	import { agentFormSchema, type AgentFormSchema } from '$lib/schema';
	import { type SuperValidated } from 'sveltekit-superforms';
	import { toast } from 'svelte-sonner';

	export let data: SuperValidated<AgentFormSchema>;

	const { form: formAgent, errors } = superForm(data, {
		validators: agentFormSchema
	});

	export let form;

	const dispatch = createEventDispatcher();

	let state: 'loading' | 'error' | 'idle' = 'idle';

	let open = false;
	const handleTrigger = async () => {
		open = true;
	};

	let published = false;

	console.log($formAgent, 'agent form');
	console.log($errors, 'agent data');
</script>

<Dialog.Root {open} onOpenChange={(o) => dispatch('close')}>
	<Dialog.Trigger class={buttonVariants({ variant: 'outline' })} on:click={handleTrigger}
		>Create Agent</Dialog.Trigger
	>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>
			<Dialog.Title>Create Agent</Dialog.Title>
		</Dialog.Header>
		<form action="?/creatAgents" method="POST" use:enhance>
			<div class="p-6">
				<div class="flex w-full items-center gap-4">
					<div class="mb-4 w-full">
						<Label for="title" class="block text-sm font-medium ">Title</Label>
						<Input
							id="title"
							name="title"
							bind:value={$formAgent.title}
							placeholder="Agent's title"
							class="border-input placeholder:text-muted-foreground focus-visible:ring-ring col-span-3 mt-1  block  h-9 w-full  rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
						/>
					</div>
					<div class="border-primary mb-4 mt-4 flex cursor-pointer items-center gap-4 p-2">
						<Toggle
							id="publishedToggle"
							name="published"
							on:click={() => (published = !published)}
							class="border-primary h-7 scale-125 transform cursor-pointer border"
						>
							<Label
								for="publishedToggle"
								class="text-on-background cursor-pointer  font-semibold italic">published</Label
							>
						</Toggle>

						<!-- Hidden input to capture the toggle state -->
						<Input type="hidden" name="published" value={published} />
					</div>
				</div>
				{#if $errors.title}
					<p class="mb-2 text-red-500">{$errors.title}</p>
				{/if}
				<div class="mb-4">
					<Label for="role" class="block text-sm font-medium ">Role</Label>
					<Input
						id="role"
						name="role"
						bind:value={$formAgent.role}
						placeholder="Agent's role"
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring col-span-3 mt-1  block  h-9 w-full  rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>
				{#if $errors.role}
					<p class="mb-2 text-red-500">{$errors.role}</p>
				{/if}
				<div class="mb-4">
					<Label for="description" class="block text-sm font-medium ">Description</Label>
					<Textarea
						id="description"
						name="description"
						bind:value={$formAgent.description}
						placeholder="Describe the agent's purpose"
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring
					col-span-3 mt-1  block h-24 w-full resize-none rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50 [&::-webkit-scrollbar]:hidden"
					></Textarea>
				</div>
				{#if $errors.description}
					<p class="mb-2 text-red-500">{$errors.description}</p>
				{/if}
				<div class="flex w-full gap-4">
					<div class="mb-4 flex w-full flex-col">
						<Label for="models" class="text-on-background mb-2 font-semibold">Models</Label>
						<select
							id="models"
							name="model"
							class="bg-surface text-on-surface block w-full rounded-lg"
						>
							<option value="gpt-4-turbo-preview">GPT-4</option>
							<option value="gpt-3.5-turbo">GPT-3.5</option>
						</select>
					</div>
				</div>
				<Button
					type="submit"
					variant="outline"
					on:click={() => {
						state = 'loading';

						if (
							$formAgent.title.length > 0 &&
							$formAgent.role.length > 0 &&
							$formAgent.description.length > 0
						) {
							state = 'idle';
							toast.success('Agent created please reload the page to see it.');

							open = false;
							invalidateAll();
						} else {
							state = 'idle';
						}
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
