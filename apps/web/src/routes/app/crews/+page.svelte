<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { timeSince } from '$lib/utils';
	import Create from './Create.svelte';
	import CreateForm from './CreateForm.svelte';

	export let data;
</script>

<div class="min-h-screen bg-background p-8">
	<div class="grid grid-cols-1 gap-10 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
		<Create>
			<CreateForm formCreate={data.form.create} />
		</Create>
		{#each data.crews as crew (crew.id)}
			<a
				href={`/app/crews/${crew.id}`}
				class="group relative flex aspect-[3/4] flex-col items-center justify-center overflow-hidden rounded-lg bg-surface text-center shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<object
					class="object-cover object-right"
					data="https://images.unsplash.com/photo-1608303588026-884930af2559?q=80&w=2006&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
					title="Crew Fallback Avatar"
					type="image/avif"
				>
					<img
						src={crew.avatar}
						alt={`Crew Avatar`}
						class="flex w-full flex-1 items-center justify-center object-cover object-bottom transition-transform duration-500 group-hover:scale-105"
					/>
				</object>
				<div class="absolute bottom-0 left-0 right-0 flex flex-grow flex-col bg-black/60 p-4">
					<h3 class="text-on-surface text-lg font-semibold duration-500 group-hover:scale-110">
						{crew.title}
					</h3>
					<p class="text-on-surface/80 mt-2 flex-grow text-sm duration-500 group-hover:scale-110">
						{crew.description.slice(0, 100)}
					</p>
				</div>
			</a>
		{/each}
	</div>
</div>
