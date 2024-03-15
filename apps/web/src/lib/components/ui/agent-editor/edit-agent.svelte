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
	import { Toggle } from '$lib/components/ui/toggle/index.js';
	import { createEventDispatcher } from 'svelte';
	import { toast } from 'svelte-sonner';

	export let form;

	let state: 'loading' | 'error' | 'idle' = 'idle';

	const dispatch = createEventDispatcher();

	export let selectedAgent: Agent;

	let published = false;

	export let open = false;

	const handleChange = () => {
		dispatch('close');
		open = !open;

		console.log(open, 'hanlde change');
	};

	console.log(form, 'from from edit');
</script>

<Dialog.Root {open} onOpenChange={handleChange}>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>
			<Dialog.Title>Edit Agent</Dialog.Title>
		</Dialog.Header>
		<form action="?/editAgent&id=${selectedAgent.id}" method="POST" use:enhance>
			<div class="p-6">
				<div class="flex w-full items-center gap-4">
					<div class="mb-4 w-full">
						<Label for="title" class="block text-sm font-medium ">Title</Label>
						<Input
							id="title"
							name="title"
							value={selectedAgent.title}
							placeholder="Agent's title"
							class="border-input placeholder:text-muted-foreground focus-visible:ring-ring col-span-3 mt-1  block  h-9 w-full  rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
						/>
					</div>
					<div class=" mb-4 mt-4 flex cursor-pointer items-center gap-4 p-2">
						<Toggle
							id="publishedToggle"
							name="published"
							value="true"
							bind:pressed={selectedAgent.published}
							on:click={() => {
								if (selectedAgent.published !== true) {
									published = true;
								} else {
									published = false;
								}
							}}
							class="border-primary h-7 scale-125 transform cursor-pointer"
						>
							<Label
								for="publishedToggle"
								class="text-on-background cursor-pointer  font-semibold italic">published</Label
							>
						</Toggle>

						<!-- Hidden input to capture the toggle state -->
						<input type="hidden" name="published" value={published} />
					</div>
				</div>
				<div class="mb-4">
					<Label for="role" class="block text-sm font-medium ">Role</Label>
					<Input
						id="role"
						name="role"
						placeholder="Agent's role"
						value={selectedAgent.role}
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring col-span-3 mt-1  block  h-9 w-full  rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>
				<div class="mb-4">
					<Label for="description" class="block text-sm font-medium ">Description</Label>
					<Textarea
						id="description"
						name="description"
						value={selectedAgent.description.join(', ')}
						placeholder="Describe the agent's purpose"
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring
					col-span-3 mt-1  block h-24 w-full resize-none rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50 [&::-webkit-scrollbar]:hidden"
					></Textarea>
				</div>
				<div class="flex w-full flex-col">
					<Label for="models" class="text-on-background mb-2 font-semibold">Models</Label>
					<select
						id="models"
						name="model"
						value={selectedAgent.model}
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
				on:click={() => (state = 'loading')}
				class="flex"
				on:click={() => {
					setTimeout(() => {
						if (form?.message) {
							toast.success(form.message + " " + " Please Reload the page to see the changes you made");
						}
						state = 'idle';
						open = false;
						invalidateAll();
					}, 2000);
					// }
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
