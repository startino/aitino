<script lang="ts">
	import CreateForm from './CreateForm.svelte';
	import UpdateForm from './UpdateForm.svelte';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import api from '$lib/api';
	import { toast } from 'svelte-sonner';
	import * as Library from '$lib/components/ui/library';

	export let data;

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

	let open = false;
</script>

<Library.Root>
	<Library.CreateButton>
		<CreateForm formCreate={data.form.agent} />
	</Library.CreateButton>
	{#each data.agents as agent}
		<Dialog.Root {open}>
			<Dialog.Trigger>
				<Library.Entry on:click={() => (open = true)} avatar={agent.avatar}>
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
								This action cannot be undone. This will permanently delete this agent from our
								services. Make sure to delete the agent from all of your own crews before you
								perform this action.
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
			</Dialog.Trigger>
			<Dialog.Content>
				<UpdateForm {agent} formUpdate={data.form.agent} />
			</Dialog.Content>
		</Dialog.Root>
	{/each}
</Library.Root>
