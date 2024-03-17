<script lang="ts">
	import type { Agent } from '$lib/types/models';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Loader2 } from 'lucide-svelte';
	import { applyAction, enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { createEventDispatcher } from 'svelte';
	import { toast } from 'svelte-sonner';
	import type { ActionData } from '../../../../routes/app/editor/agent/$types';
	import { AgentEditorItems } from '$lib/components/ui/agent-editor-items';

	export let form: ActionData;

	let state: 'loading' | 'error' | 'idle' = 'idle';

	const dispatch = createEventDispatcher();

	export let selectedAgent: Agent;

	export let open = false;

	const handleChange = () => {
		dispatch('close');
		open = !open;
	};
	$: isFormIncomplete =
		!selectedAgent?.title || !selectedAgent?.role || !selectedAgent?.description;

</script>

<Dialog.Root {open} onOpenChange={handleChange}>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<Dialog.Header>
			<Dialog.Title>Edit Agent</Dialog.Title>
		</Dialog.Header>
		<form
			action="?/editAgent&id=${selectedAgent.id}"
			method="POST"
			use:enhance={() => {
				return async ({ result }) => {
					invalidateAll();
					state = 'idle';
					applyAction(result);
				};
			}}
		>
			<AgentEditorItems {selectedAgent} isCreate={false} />
			<Button
				type="submit"
				disabled={isFormIncomplete}
				variant="outline"
				class="flex"
				on:click={() => {
					state = 'loading';
					setTimeout(() => {
						console.log(form);
						if (form?.message) {
							toast.promise(invalidateAll(), {
								loading: 'Editing...',
								success: `${form?.message}`,
								error: 'Error'
							});

							setTimeout(() => {
								state = 'idle';
								open = false;
								location.reload();
							}, 1000);
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
