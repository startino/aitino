<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { timeSince } from '$lib/utils';
	import Create from './Create.svelte';
	import CreateForm from './CreateForm.svelte';

	export let data;
</script>

<div class="min-h-screen bg-background p-8">
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		<Create>
			<CreateForm formCreate={data.form.create} />
		</Create>
		{#each data.crews as crew (crew.id)}
			<div
				class="group relative flex flex-col items-center justify-center overflow-hidden rounded-lg bg-surface shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<img
					src={crew.avatar}
					alt={`Crew Avatar`}
					class="flex w-full flex-1 items-center justify-center object-cover"
				/>
				<div class="p-4">
					<h3 title={crew.title} class="mb-2 line-clamp-1 text-ellipsis text-lg font-semibold">
						{crew.title}
					</h3>
					<p class="mb-4 line-clamp-3 text-ellipsis text-sm">{crew.description}</p>
					<div class="mb-3 text-sm text-gray-600">
						<p>Created {timeSince(crew.created_at)} ago</p>
						<p>Updated {timeSince(crew.updated_at)} ago</p>
					</div>
					<div class="flex w-full items-center justify-center gap-4">
						<Button href="/app/crews/{crew.id}" class="w-full">Open</Button>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>
