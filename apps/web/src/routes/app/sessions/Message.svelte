<script lang="ts">
	import { User } from 'lucide-svelte';
	import SvelteMarkdown from 'svelte-markdown';
	import * as models from '$lib/types/models';
	import * as Avatar from '$lib/components/ui/avatar';
	import * as utils from '$lib/utils';
	import { onMount } from 'svelte';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import Agent from '$lib/components/ui/custom-node/agent.svelte';
	import { fade, fly, slide } from 'svelte/transition';

	export let message: models.Message;

	function formatName(inputString: string): string {
		return inputString
			.replace(/([a-z])([A-Z])/g, '$1 $2')
			.replace(/([A-Z])([A-Z][a-z])/g, '$1 $2')
			.replace(/-/g, ' - ');
	}

	let agent: Promise<models.Agent> | null = null;

	async function getAgent(agentId: string) {
		const res = await fetch(`/api/get-agent?agentId=${agentId}`);
		const data = await res.json();
		return data.agent as models.Agent;
	}

	onMount(() => {
		agent = getAgent(message.sender_id);
	});
</script>

<div
	class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg flex max-w-none flex-col items-start justify-end px-12"
>
	{#if agent}
		{#await agent}
			<div class="flex w-full justify-center gap-3">
				<Skeleton class="h-10 w-10" />

				<div class="flex w-full items-end justify-between gap-4">
					<Skeleton class="h-full w-[200px]" />
					<Skeleton class="h-full w-[100px]" />
				</div>
			</div>
		{:then agent}
			<div class="flex w-full flex-row place-items-center gap-3">
				<Avatar.Root class="not-prose">
					<Avatar.Image src={agent.avatar_url} />
					<Avatar.Fallback>IMG</Avatar.Fallback>
				</Avatar.Root>

				<div class="flex w-full items-end justify-between gap-4">
					<h2 class="m-0 sm:m-0">{agent.name}</h2>
					<p class="m-0 sm:m-0">
						{utils.getLocalTime(message.created_at)}
					</p>
				</div>
			</div>
		{:catch error}
			<div class="flex w-full justify-center gap-3">
				<p>Error: {error.message}</p>
			</div>
		{/await}
		<SvelteMarkdown source={message.content} />
	{:else}
		Couldn't get the agent from the database.
	{/if}
</div>
