<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import * as models from '$lib/types/models';
	import * as Avatar from '$lib/components/ui/avatar';
	import * as utils from '$lib/utils';
	import { onMount } from 'svelte';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import type { ActionResult } from '@sveltejs/kit';
	import { applyAction, deserialize } from '$app/forms';
	import { invalidateAll } from '$app/navigation';

	export let message: models.Message;

	let agent: models.Agent = {
		id: null,
		created_at: Date.now().toString(),
		updated_at: Date.now().toString(),
		title: 'Admin',
		description: 'Acts as the user and admin of the conversation',
		role: 'Admin',
		author: 'Futino',
		model: 'N/A',
		published: false,
		system_message: 'N/A',
		profile_id: 'N/A',
		tools: [],
		avatar:
			'https://ommkphtudcxplovqfhmu.supabase.co/storage/v1/object/public/agent-avatars/11.png',
		version: '1'
	};

	async function getAgent(agentId: string) {
        console.log(`trying to get agent with id ${agentId}`);

        const agent: models.Agent = await fetch(`?/getagent?agent-id=${agentId}`, { method: 'GET'
        }).then((res) => {
            console.log(`got response on ${agentId}: ${JSON.stringify(res)}`);
            return res.json()
        }).then((data) => {
            console.log(`got response on ${agentId}: ${JSON.stringify(data)}`);
            return data.agent;
        }).catch((error) => {
            console.error('Failed to fetch agent:', error);
            return {
                id: null,
                created_at: Date.now().toString(),
                updated_at: Date.now().toString(),
                title: 'Error',
                description: 'Error fetching agent data',
                role: 'error agent',
                author: 'Futino',
                model: 'N/A',
                published: false,
                system_message: 'N/A',
                profile_id: 'N/A',
                tools: [],
                avatar:
                    'https://ommkphtudcxplovqfhmu.supabase.co/storage/v1/object/public/agent-avatars/11.png',
                version: '1'
            } as models.Agent;
        });

        console.log(`got response on ${agentId}: ${JSON.stringify(agent)}`);
        return agent;
	}

	async function loadAgent() {
		if (message.sender_id) {
			agent = await getAgent(message.sender_id);
		}
	}

	onMount(() => {
		loadAgent();
	});
</script>

<div
	class="xl:prose-md prose prose-sm prose-main flex max-w-none flex-col items-start justify-end px-12 md:prose-base 2xl:prose-lg"
>
	{#if agent}
		<div class="flex w-full flex-row place-items-center gap-3">
			<Avatar.Root class="not-prose">
				<Avatar.Image src={agent.avatar} />
				<Avatar.Fallback>IMG</Avatar.Fallback>
			</Avatar.Root>

			<div class="flex w-full items-end justify-between gap-4">
				<h2 class="m-0 sm:m-0">{agent.title}</h2>
				<p class="m-0 sm:m-0">
					{utils.getLocalTime(message.created_at)}
				</p>
			</div>
		</div>
		<SvelteMarkdown source={message.content} />
	{:else}
		<div class="flex w-full justify-center gap-3">
			<Skeleton class="h-10 w-10" />

			<div class="flex w-full items-end justify-between gap-4">
				<Skeleton class="h-full w-[200px]" />
				<Skeleton class="h-full w-[100px]" />
			</div>
		</div>
	{/if}
</div>
