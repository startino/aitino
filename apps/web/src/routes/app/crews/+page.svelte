<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import type { Crew } from '$lib/types/models';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Switch } from '$lib/components/ui/switch';
	import { timeSince } from '$lib/utils';
	import { Textarea } from '$lib/components/ui/textarea';
	import { enhance } from '$app/forms';
	import { toast } from 'svelte-sonner';
	import { invalidateAll } from '$app/navigation';
	import { Loader2 } from 'lucide-svelte';
	import type { ActionData, PageData } from './$types';

	export let data: PageData;
	export let form: ActionData;

	$: myCrews = data.data as ArrayLike<unknown> | Iterable<unknown>;

	let selectedcrew: Crew;
	let open = false;
	let state: 'idle' | 'loading' | 'error' = 'idle';

	const editcrew = async (crew: Crew) => {
		selectedcrew = crew;
		open = true;
	};

	$: handleSubmit = async () => {
		console.log(form, 'form');

		if (form?.success) {
			toast.promise(invalidateAll(), {
				loading: 'Saving changes...',
				success: 'Changes saved successfully',
				error: 'An error occurred while saving changes'
			});

			state = 'idle';
			open = false;
		}
	};

	$: handleSubmit();
</script>

<div class="bg-background min-h-screen p-8">
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		{#each myCrews as crew}
			<div
				class="bg-surface group relative flex flex-col overflow-hidden rounded-lg shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<div class="flex-shrink-0">
					<img
						src={crew.avatar}
						alt={`Avatar of ${crew.title}`}
						class="h-48 w-full object-cover transition-transform duration-500 group-hover:scale-110"
					/>
				</div>
				<div class="flex flex-grow flex-col p-4">
					<div class="flex justify-between">
						<h3 class="text-on-surface text-lg font-semibold">{crew.title}</h3>
					</div>
					<p class="text-on-surface/80 mt-2 flex-grow text-sm">{crew.description}</p>
					<div class="mt-4 text-sm text-gray-600">
						<p>Created: {timeSince(new Date(crew.created_at))} ago</p>
						<p>Updated: {timeSince(new Date(crew.updated_at))} ago</p>
					</div>
				</div>
				<div class="flex w-full items-center justify-center gap-4">
					<Button
						class="w-full"
						on:click={() => {
							window.open(`/app/crews/${crew.id}`, '_self');
						}}>Load</Button
					>
					<Button
						class="text-md w-full font-semibold transition-colors duration-300"
						on:click={() => {
							editcrew(crew);
						}}>Edit</Button
					>
				</div>
			</div>
		{/each}
	</div>
</div>

<Dialog.Root {open} onOpenChange={(o) => (open = o)}>
	<Dialog.Content class="sm:max-w-[425px]">
		<Dialog.Header>
			<Dialog.Title>Edit crew</Dialog.Title>
		</Dialog.Header>
		<form class="p-3" action="?/editCrew&id={selectedcrew.id}" method="POST" use:enhance>
			<div class="mb-2 flex w-full items-center gap-2">
				<div class="w-full space-y-4">
					<Label for="title" class="text-right">Title</Label>
					<Input
						id="title"
						name="title"
						bind:value={selectedcrew.title}
						class="col-span-3 focus-visible:ring-1 focus-visible:ring-offset-0"
					/>
				</div>
				<div class="mt-8 flex items-center space-x-2">
					<Label for="published" class="flex items-center">
						<Switch id="published" name="published" bind:checked={selectedcrew.published} />
						<span class="ml-2 text-sm text-gray-700">Published</span>
					</Label>
				</div>
			</div>
			{#if selectedcrew.title.trim().length === 0}
				<p class="text-red-500">Title is required</p>
			{/if}
			<div class="mb-2 flex w-full items-center gap-2">
				<div class="w-full space-y-4">
					<Label for="description" class="text-right">Description</Label>
					<Textarea
						id="description"
						name="description"
						bind:value={selectedcrew.description}
						class="block h-24 w-full resize-none focus-visible:ring-1 focus-visible:ring-offset-0 [&::-webkit-scrollbar]:hidden"
					></Textarea>
				</div>
			</div>
			{#if selectedcrew.description.trim().length === 0}
				<p class="text-red-500">Description is required</p>
			{/if}
			<Dialog.Footer>
				<Button
					disabled={selectedcrew.title.trim().length === 0 ||
						selectedcrew.description.trim().length === 0}
					type="submit"
					on:click={() => {
						state = 'loading';
					}}
				>
					{#if state === 'loading'}
						<Loader2 class="mr-2 mt-1 h-4 w-4 animate-spin" />
					{/if} Save changes</Button
				>
			</Dialog.Footer>
		</form></Dialog.Content
	>
</Dialog.Root>
