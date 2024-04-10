<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Switch } from '$lib/components/ui/switch';
	import { timeSince } from '$lib/utils';
	import { Textarea } from '$lib/components/ui/textarea';
	import { toast } from 'svelte-sonner';
	import { Loader2 } from 'lucide-svelte';
	import { superForm } from 'sveltekit-superforms/client';

	export let data;

	const { form, errors, enhance } = superForm(data.form, {
		onUpdated({ form }) {
			if (form.valid) {
				open = false;
				toast.success(form.message);
			}

			state = 'idle';
		}
	});

	let open = false;
	let state: 'idle' | 'loading' | 'error' = 'idle';
</script>

<div class="grid grid-cols-[repeat(auto-fill,_minmax(250px,_1fr))] gap-4 p-8">
	{#each data.crews as crew (crew.id)}
		<div class="bg-card rounded-lg">
			<img src={crew.avatar} alt={`Avatar of ${crew.title}`} class="h-32 w-full object-cover" />
			<div class="p-4">
				<h3 title={crew.title} class="mb-2 line-clamp-1 text-ellipsis text-lg font-semibold">
					{crew.title}
				</h3>
				<p class="mb-4 line-clamp-3 text-ellipsis text-sm">{crew.description}</p>
				<div class="mb-3 text-sm text-gray-600">
					<p>Created {timeSince(crew.created_at)} ago</p>
					<p>Updated {timeSince(crew.updated_at)} ago</p>
				</div>
				<div class="flex w-full items-center justify-center gap-4">
					<Button href="/app/crews/{crew.id}" class="w-full">Load</Button>
					<Button
						class="w-full"
						variant="outline"
						on:click={() => {
							$form = {
								id: crew.id,
								title: crew.title,
								description: crew.description,
								published: crew.published
							};
							open = true;
						}}>Edit</Button
					>
				</div>
			</div>
		</div>
	{/each}
</div>

<Dialog.Root {open} onOpenChange={(o) => (open = o)}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Edit crew</Dialog.Title>
		</Dialog.Header>

		<form
			class="p-4"
			action="?/editCrew"
			method="POST"
			on:submit={() => (state = 'loading')}
			use:enhance
		>
			<div class="mb-2 flex w-full items-center gap-2">
				<div class="w-full space-y-4">
					<Label for="title" class="text-right">Title</Label>
					<input bind:value={$form.id} name="id" hidden />
					<Input
						name="title"
						bind:value={$form.title}
						class="col-span-3 focus-visible:ring-1 focus-visible:ring-offset-0"
					/>
				</div>
				<div class="mt-8 flex items-center space-x-2">
					<Label for="published" class="flex items-center">
						<Switch id="published" name="published" bind:checked={$form.published} />
						<span class="ml-2 text-sm text-gray-700">Published</span>
					</Label>
				</div>
			</div>
			{#if $errors.title}
				<p class="text-red-500">{$errors.title[0]}</p>
			{/if}
			<div class="mb-2 flex w-full items-center gap-2">
				<div class="w-full space-y-4">
					<Label for="description" class="text-right">Description</Label>
					<Textarea
						id="description"
						name="description"
						bind:value={$form.description}
						class="block h-24 w-full resize-none focus-visible:ring-1 focus-visible:ring-offset-0 [&::-webkit-scrollbar]:hidden"
					></Textarea>
				</div>
			</div>
			{#if $errors.description}
				<p class="text-red-500">{$errors.description[0]}</p>
			{/if}
			{#if $errors._errors}
				<p class="text-red-500">{$errors._errors[0]}</p>
			{/if}
			<Dialog.Footer>
				<Button type="submit">
					{#if state === 'loading'}
						<Loader2 class="mr-2 mt-1 h-4 w-4 animate-spin" />
					{/if}
					Save changes
				</Button>
			</Dialog.Footer>
		</form></Dialog.Content
	>
</Dialog.Root>
