<script lang="ts">
	import {enhance} from '$app/forms';
	import {Button, buttonVariants} from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import {Input} from '$lib/components/ui/input';
	import {Label} from '$lib/components/ui/label';
	import {Textarea} from '$lib/components/ui/textarea';
	import {Loader2} from 'lucide-svelte';

	let state: 'loading' | 'error' | 'idle' = 'idle';

	let open = false;
	const handleTrigger = async () => {
		open = true;
	};
</script>

<Dialog.Root {open} onOpenChange={(o) => (open = o)}>
	<Dialog.Trigger class={buttonVariants({variant: 'outline'})} on:click={handleTrigger}
		>Create Agent</Dialog.Trigger
	>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>
			<Dialog.Title>Create Agent</Dialog.Title>
		</Dialog.Header>
		<form action="?/creatAgents" method="POST" use:enhance>
			<div class="p-6">
				<div class="mb-4">
					<Label for="title" class="block text-sm font-medium ">Title</Label>
					<Input
						id="title"
						name="title"
						placeholder="Agent's title"
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring col-span-3 mt-1  block  h-9 w-full  rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>
				<div class="mb-4">
					<Label for="role" class="block text-sm font-medium ">Role</Label>
					<Input
						id="role"
						name="role"
						placeholder="Agent's role"
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring col-span-3 mt-1  block  h-9 w-full  rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50"
					/>
				</div>
				<div class="mb-4">
					<Label for="description" class="block text-sm font-medium ">Description</Label>
					<Textarea
						id="description"
						name="description"
						placeholder="Describe the agent's purpose"
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring
					col-span-3 mt-1  block h-24 w-full resize-none rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50 [&::-webkit-scrollbar]:hidden"
					></Textarea>
				</div>
				<div class="mb-4">
					<Label for="tools" class="block text-sm font-medium ">Tools</Label>
					<Textarea
						id="tools"
						name="tools"
						placeholder="List the tools the agent uses"
						class="border-input placeholder:text-muted-foreground focus-visible:ring-ring
					col-span-3 mt-1  block h-24 w-full resize-none rounded-md border bg-transparent px-3 text-sm shadow-sm ring-offset-0 transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50 [&::-webkit-scrollbar]:hidden"
					></Textarea>
				</div>
				<div class="flex flex-col">
					<Label for="models" class="text-on-background mb-2 font-semibold">Models</Label>
					<select
						id="models"
						name="model"
						class="bg-surface text-on-surface block w-full rounded-lg"
					>
						<option value="gpt-4-turbo-preview">GPT-4</option>
						<option value="gpt-3.5-turbo-preview">GPT-3.5</option>
					</select>
				</div>
			</div>
			<Button
				type="submit"
				variant="outline"
				on:click={() => ((state = 'loading'), (open = false))}
				class="flex"
			>
				Create

				{#if state === 'loading'}
					<Loader2 class="ml-2 w-4 animate-spin" />
				{/if}
			</Button>
		</form>
	</Dialog.Content>
</Dialog.Root>
