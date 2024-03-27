<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Loader2, Plus } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';
	import { superForm } from 'sveltekit-superforms/client';
	import { createNewAgents, type AgentFormSchema } from '$lib/schema';
	import { type SuperValidated } from 'sveltekit-superforms';
	import { toast } from 'svelte-sonner';
	import { AgentEditorItems } from '$lib/components/ui/agent-editor-items';
	import type { ActionData } from '../../../../routes/app/editor/agent/$types';
	import type { Agent } from '$lib/types/models';

	export let data: SuperValidated<AgentFormSchema>;
	export let agentTools: string[] | null;
	export let apiKeyTypes: string[] | null;
	export let user_api_keys: string[] | null;
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
	<!-- <div>
		
	</div> -->
	<Dialog.Trigger
		on:click={handleTrigger}
		class="to-primary-800 bg-background transition-hover from-primary-950 group relative flex  flex-col overflow-hidden rounded-lg shadow-lg duration-1000 hover:scale-105 hover:bg-gradient-to-br hover:shadow-xl"
	>
		<Plus
			class=" absolute left-[50%] top-[50%] z-10 flex-shrink-0 translate-x-[-50%] translate-y-[-50%] transition-all duration-300 "
			size="120"
		/>
	</Dialog.Trigger>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<form action="?/creatAgents" method="POST" use:enhance>
			<AgentEditorItems
				{errors}
				{formAgent}
				isCreate={true}
				{agentTools}
				{apiKeyTypes}
				{user_api_keys}
			/>
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
