<script lang="ts">
	import Create from './Create.svelte';
	import CreateForm from './CreateForm.svelte';
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import { Button } from '$lib/components/ui/button';
	import { X } from 'lucide-svelte';
	import api from '$lib/api';
	import { toast } from 'svelte-sonner';

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
</script>

<div class="min-h-screen bg-background p-8">
	<div class="grid grid-cols-1 gap-10 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
		<Create>
			<CreateForm formCreate={data.form.create} />
		</Create>
		{#each data.agents as agent}
			<div
				class="group relative flex aspect-[3/4] flex-col items-center justify-center overflow-hidden rounded-lg bg-surface text-center shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<img
					src={agent.avatar}
					alt={`Agent Avatar`}
					class="flex w-full flex-1 items-center justify-center object-cover object-bottom transition-transform duration-500 group-hover:scale-105"
				/>
				<div class="absolute bottom-0 left-0 right-0 flex flex-grow flex-col bg-background/60 p-4">
					<h3 class="text-on-surface text-lg font-semibold duration-500 group-hover:scale-110">
						{agent.title}
					</h3>
					<p class="text-on-surface/80 mt-2 flex-grow text-sm duration-500 group-hover:scale-110">
						{agent.role}
					</p>
				</div>
				<!-- delete -->
				<AlertDialog.Root>
					<AlertDialog.Trigger>
						<button
							type="button"
							class="absolute right-4 top-4 z-10 rounded-sm text-white hover:scale-125 disabled:pointer-events-none"
						>
							<X />
							<span class="sr-only">Close</span></button
						>
					</AlertDialog.Trigger>
					<AlertDialog.Content>
						<AlertDialog.Header>
							<AlertDialog.Title>Are you sure absolutely sure?</AlertDialog.Title>
							<AlertDialog.Description>
								This action cannot be undone. This will permanently delete this crew and it's
								sessions from our services.
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
					</AlertDialog.Content>
				</AlertDialog.Root>
			</div>
		{/each}
	</div>
</div>
