<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Loader2 } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import { superForm } from 'sveltekit-superforms/client';
	import { createNewAgents, type AgentFormSchema } from '$lib/schema';
	import { type SuperValidated } from 'sveltekit-superforms';
	import { toast } from 'svelte-sonner';
	import { AgentEditorItems } from '$lib/components/ui/agent-editor-items';
	import type { ActionData } from '../../../../routes/app/editor/agent/$types';

	export let data: SuperValidated<AgentFormSchema>;
	export let agentTools;

	const { form: formAgent, errors } = superForm(data, {
		validators: createNewAgents
	});

	export let form: ActionData;

	const dispatch = createEventDispatcher();

	let state: 'loading' | 'error' | 'idle' = 'idle';

	let open = false;
	const handleTrigger = async () => {
		open = true;
	};
</script>

<Dialog.Root {open} onOpenChange={(o) => dispatch('close')}>
	<div class="absolute bottom-5 right-5">
		<Dialog.Trigger class={buttonVariants({ variant: 'outline' })} on:click={handleTrigger}>
			Create Agent
		</Dialog.Trigger>
	</div>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<!-- <Dialog.Header>
			<Dialog.Title>Create Agent</Dialog.Title>
		</Dialog.Header> -->
		<form action="?/creatAgents" method="POST" use:enhance>
			<AgentEditorItems {errors} {formAgent} isCreate={true} {agentTools} />
			<Button
				type="submit"
				variant="outline"
				on:click={() => {
					state = 'loading';
					console.log($errors, $formAgent);
					setTimeout(() => {
						state = 'idle';
						open = false;
						toast.success(form?.message);
					}, 2000);
				}}
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
