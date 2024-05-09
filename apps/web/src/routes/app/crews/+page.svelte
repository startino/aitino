<script lang="ts">
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import CreateForm from './CreateForm.svelte';
	import * as Library from '$lib/components/ui/library';
	import { Button } from '$lib/components/ui/button/index.js';
	import api from '$lib/api';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import { getContext } from '$lib/context';

    let { crews } = getContext('root');

	const deleteCrew = (id: string) => {
		api
			.DELETE('/crews/{id}', {
				params: {
					path: { id }
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					toast(`Error deleting crew ${id}: ${e.detail}`);
				}
				if (!d) {
					toast(`No data returned from crew deletion`);
				}
				return d;
			});
	};
</script>

<Library.Root>
	<Library.CreateButton>
		<CreateForm />
	</Library.CreateButton>
	{#each $crews as crew (crew.id)}
		<Library.Entry
			on:click={() => goto(`/app/crews/${crew.id}`)}
			avatar={'https://images.unsplash.com/photo-1608303588026-884930af2559'}
		>
			<div slot="content">
				<Library.EntryHeader>
					{crew.title}
				</Library.EntryHeader>
				<Library.EntryContent>
					{crew.description.slice(0, 100)}
				</Library.EntryContent>
			</div>
			<div slot="delete">
				<AlertDialog.Header>
					<AlertDialog.Title>Are you sure absolutely sure?</AlertDialog.Title>
					<AlertDialog.Description>
						This action cannot be undone. This will permanently delete this crew and it's sessions
						from our services.
					</AlertDialog.Description>
				</AlertDialog.Header>
				<AlertDialog.Footer>
					<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
					<Button
						on:click={() => {
							deleteCrew(crew.id);
							$crews = $crews.filter((c) => c.id !== crew.id);
						}}
						variant="destructive"
						class="bg-red-900">Delete</Button
					>
				</AlertDialog.Footer>
			</div>
		</Library.Entry>
	{/each}
</Library.Root>
