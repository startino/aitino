<script lang="ts">
	import { CreateAgent, EditAgent } from '$lib/components/ui/agent-editor/';
	import type { Agent } from '$lib/types/models';
	import { Button } from '$lib/components/ui/button';

	export let data;
	export let form;

	$: myAgents = (data.currentUserAgents.data as Agent[]) || [];
	$: myTools = (data.agentTools.data as Agent[]) || [];
	let open = false;

	let selectedAgent: Agent;

	const editAgent = async (agent: Agent) => {
		selectedAgent = agent;
		open = true;
	};

	const handleClose = () => {
		open = false;
	};
</script>

<div class="bg-background min-h-screen p-8">
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		{#each myAgents as agent}
			<div
				class="bg-surface group relative flex flex-col overflow-hidden rounded-lg shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
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
					class="text-md bg-primary text-background hover:bg-primary/90 mt-4 w-full rounded-none p-2 font-semibold transition-colors duration-300"
					on:click={() => {
						editAgent(agent);
					}}>Edit Agent</Button
				>
			</div>
		{/each}
		<CreateAgent
			on:close={() => (open = false)}
			{form}
			data={data.agentForm}
			agentTools={myTools}
			apiKeyTypes={data.api_key_types}
			user_api_keys={data.user_api_keys}
		/>
	</div>
</div>

<!-- <ComingSoonPage releaseVersion="v0.3.0" /> -->

<EditAgent
	{selectedAgent}
	on:close={handleClose}
	{open}
	{form}
	agentTools={myTools}
	apiKeyTypes={data.api_key_types}
	user_api_keys={data.user_api_keys}
/>
