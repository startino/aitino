<script lang="ts">
	import { ComingSoonPage } from '$lib/components/ui/coming-soon';
	import CreateAgent from '$lib/components/ui/create-agent/create-agent.svelte';
	import type { Agent } from '$lib/types/models';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Loader2 } from 'lucide-svelte';
	import { applyAction, enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';

	let state: 'loading' | 'error' | 'idle' = 'idle';
	export let data;
	export let form;

	let myAgents: Agent[] = data.getCurrentUserAgents.data;
	let open = false;
	const handleTrigger = async () => {
		open = true;
	};

	let selectedAgent: Agent;

	const editAgent = async (agent: Agent) => {
		console.log(agent);
		selectedAgent = agent;
		open = true;
	};
</script>

<div class="bg-background min-h-screen p-8">
	<h1 class="text-primary dark:text-primary/80 mb-8 text-center text-4xl font-bold">
		<span class="from-accent to-secondary bg-gradient-to-r bg-clip-text text-transparent"
			>My Agent</span
		>
	</h1>
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		{#each myAgents as agent}
			<div
				class="bg-surface group relative flex flex-col overflow-hidden rounded-lg shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<div class="flex-shrink-0">
					<img
						src={agent.avatar}
						alt={`Avatar of ${agent.title}`}
						class="h-48 w-full object-cover transition-transform duration-500 group-hover:scale-110"
					/>
				</div>
				<div class="flex flex-grow flex-col p-4">
					<div class="flex justify-between">
						<h3 class="text-on-surface text-lg font-semibold">{agent.title}</h3>
					</div>
					<p class="text-on-surface/80 mt-2 flex-grow text-sm">{agent.role}</p>
				</div>
				<button
					class="bg-primary text-on-primary hover:bg-primary/90 mt-4 w-full rounded-none p-2 text-sm font-semibold transition-colors duration-300"
					on:click={() => editAgent(agent)}>Edit Agent</button
				>
			</div>
		{/each}
	</div>
</div>

<!-- <ComingSoonPage releaseVersion="v0.3.0" /> -->
<CreateAgent on:close={() => (open = false)} {form} />

<Dialog.Root {open} onOpenChange={(o) => (open = o)}>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>
			<Dialog.Title>Edit Agent</Dialog.Title>
		</Dialog.Header>
		<form
			action="?/editAgent&id=${selectedAgent.id}"
			method="POST"
			use:enhance={() => {
				return ({ result }) => {
					invalidateAll();
					applyAction(result);
				};
			}}
		>
			<div class="p-6">
				<div class="mb-4">
					<Label for="title" class="block text-sm font-medium ">Title</Label>
					<Input
						id="title"
						name="title"
						value={selectedAgent.title}
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
				<div class="flex flex-col">
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
			{#if form?.message}
				<p>{form.message}</p>
			{/if}
			<Button
				type="submit"
				variant="outline"
				on:click={() => (state = 'loading')}
				class="flex"
				on:click={() => {
					setTimeout(() => {
						if (form?.message) {
							state = 'idle';
							open = false;
							invalidateAll()
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
