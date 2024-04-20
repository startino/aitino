<script lang="ts">
	import Create from './Create.svelte';
	import CreateForm from './CreateForm.svelte';

	export let data;
</script>

<div class="min-h-screen bg-background p-8">
	<div class="grid grid-cols-1 gap-10 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
		<Create>
			<CreateForm formCreate={data.form.create} />
		</Create>
		{#each data.agents as agent}
			<div
				class="group relative flex aspect-[3/4] flex-col items-center justify-center overflow-hidden rounded-lg bg-surface text-center shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<img
					src={agent.avatar}
					alt={`Agent Avatar`}
					class="flex w-full flex-1 items-center justify-center object-cover object-bottom transition-transform duration-500 group-hover:scale-105"
				/>
				<div class="absolute bottom-0 left-0 right-0 flex flex-grow flex-col bg-black/60 p-4">
					<h3 class="text-on-surface text-lg font-semibold duration-500 group-hover:scale-110">
						{agent.title}
					</h3>
					<p class="text-on-surface/80 mt-2 flex-grow text-sm duration-500 group-hover:scale-110">
						{agent.role}
					</p>
				</div>
			</div>
		{/each}
	</div>
</div>
