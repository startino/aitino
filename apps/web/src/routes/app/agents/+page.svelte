<script lang="ts">
	import type { schemas } from '$lib/api';
	import Create from './Create.svelte';
	import Edit from './Edit.svelte';
	import { Button } from '$lib/components/ui/button';
	import { enhance } from '$app/forms';
	import { toast } from 'svelte-sonner';
	import { AgentEditorItems } from './components';
	import { createAgentSchema } from '$lib/schema';
	import { superForm } from 'sveltekit-superforms';

	export let data;
	export let form;

	const { form: formAgent, errors } = superForm(data.agentForm, {
		validators: createAgentSchema
	});

	$: agents =
		(data.currentUserAgents.data as schemas['Agent'] | null) ?? ([] as schemas['Agent'][]);
	$: tools = (data.agentTools.data as schemas['Tool'] | null) ?? ([] as schemas['Agent'][]);
	let open = false;

	let selectedAgent: schemas['Agent'] | null;

	const editAgent = async (agent: schemas['Agent']) => {
		selectedAgent = agent;
		open = true;
	};

	const handleClose = () => {
		open = false;
	};
</script>

<div class="min-h-screen bg-background p-8">
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		<Create on:close={() => (open = false)}>
			<form action="?/creatAgents" method="POST" use:enhance>
				<AgentEditorItems
					{errors}
					isCreate={true}
					agentTools={tools}
					apiKeyTypes={data.api_key_types ?? []}
					user_api_keys={data.user_api_keys}
				/>
				<Button
					type="submit"
					variant="outline"
					on:click={() => {
						console.log(errors, formAgent);
						setTimeout(() => {
							open = false;
							toast.success(form?.message ?? 'message not available');
						}, 2000);
					}}
					class="flex"
				>
					Create
				</Button>
			</form>
		</Create>
		{#each agents as agent}
			<div
				class="group relative flex flex-col overflow-hidden rounded-lg bg-surface shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
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
				<Button
					class="text-md mt-4 w-full rounded-none bg-primary p-2 font-semibold text-background transition-colors duration-300 hover:bg-primary/90"
					on:click={() => {
						editAgent(agent);
					}}>Edit Agent</Button
				>
			</div>
		{/each}
	</div>
</div>

<!-- <ComingSoonPage releaseVersion="v0.3.0" /> -->

<Edit
	{selectedAgent}
	on:close={handleClose}
	{open}
	{form}
	agentTools={tools}
	apiKeyTypes={data.api_key_types}
	user_api_keys={data.user_api_keys}
/>
