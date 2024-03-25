<script lang="ts">
	import SvelteMarkdown from 'svelte-markdown';
	import * as models from '$lib/types/models';
	import * as Avatar from '$lib/components/ui/avatar';
	import * as utils from '$lib/utils';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import { onMount } from 'svelte';

	export let message: models.Message;
	export let agents: models.Agent[];

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

	onMount(() => {
		agent = agents.find((a) => a.id === message.sender_id) || agent;
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
