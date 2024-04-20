<script lang="ts">
	import Create from './Create.svelte';
	import CreateForm from './CreateForm.svelte';

	export let data;
</script>

<div class="min-h-screen bg-background p-8">
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		<Create>
			<CreateForm formCreate={data.form.create} />
		</Create>
		{#each data.agents as agent}
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
			</div>
		{/each}
	</div>
</div>
