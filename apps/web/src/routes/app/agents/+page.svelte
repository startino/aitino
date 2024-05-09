<script lang="ts">
	import CreateForm from './CreateForm.svelte';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import { Button } from '$lib/components/ui/button';
	import api from '$lib/api';
	import { toast } from 'svelte-sonner';
	import * as Library from '$lib/components/ui/library';
	import { goto } from '$app/navigation';
	import { getContext } from '$lib/context';

	export let data;

	let { agents } = getContext('root');

	const deleteAgent = (id: string) => {
		api
			.DELETE('/agents/{id}', {
				params: {
					path: { id }
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					toast(`Error deleting agent ${id}: ${e.detail}`);
				}
				if (!d) {
					toast(`No data returned from agent deletion`);
				}
				return d;
			});
	};
</script>

<Library.Root>
	<Library.CreateButton>
		<CreateForm />
	</Library.CreateButton>
	{#each $agents as agent}
		<Library.Entry on:click={() => goto(`/app/agents/${agent.id}`)} avatar={agent.avatar}>
			<div slot="content">
				<Library.EntryHeader>
					{agent.title}
				</Library.EntryHeader>
				<Library.EntryContent>
					{agent.role}
				</Library.EntryContent>
			</div>
			<div slot="delete">
				<AlertDialog.Header>
					<AlertDialog.Title>Are you sure absolutely sure?</AlertDialog.Title>
					<AlertDialog.Description>
						This action cannot be undone. This will permanently delete this agent from our services.
						Make sure to delete the agent from all of your own crews before you perform this action.
					</AlertDialog.Description>
				</AlertDialog.Header>
				<AlertDialog.Footer>
					<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
					<Button
						on:click={() => {
							deleteAgent(agent.id);
							data.agents = data.agents.filter((c) => c.id !== agent.id);
						}}
						variant="destructive"
						class="bg-red-900">Delete</Button
					>
				</AlertDialog.Footer>
			</div>
		</Library.Entry>
	{/each}
</Library.Root>
