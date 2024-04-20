<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { timeSince } from '$lib/utils';
	import Create from './Create.svelte';
	import api from '$lib/api';
	import CreateForm from './CreateForm.svelte';
	// import { createCrewSchema } from '$lib/schema';
	// import { zod } from 'sveltekit-superforms/adapters';

	export let data;

	// const create = async (request: FormData) => {
	// 	const superValidated = await superValidate(request, zod(createCrewSchema));
	//
	// 	if (!superValidated.valid) {
	// 		return fail(400, { _superValidated: superValidated });
	// 	}
	//
	// 	await api
	// 		.PATCH(`/crews/{id}`, {
	// 			params: {
	// 				path: {
	// 					id: superValidated.data.id
	// 				}
	// 			},
	// 			body: {
	// 				...superValidated.data
	// 			}
	// 		})
	// 		.then(({ data: d, error: e }) => {
	// 			if (e) {
	// 				toast.error(`Error creating crew: ${e.detail}`);
	// 			}
	// 		});
	// };
</script>

<div class="min-h-screen bg-background p-8">
	<div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
		<Create>
			<CreateForm formCreate={data.form.create} />
		</Create>
		{#each data.crews as crew (crew.id)}
			<div
				class="group relative flex flex-col overflow-hidden rounded-lg bg-surface shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
			>
				<img src={crew.avatar} alt={`Avatar of ${crew.title}`} class="h-32 w-full object-cover" />
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
						<Button href="/app/crews/{crew.id}" class="w-full">Load</Button>
					</div>
				</div>
			</div>
		{/each}
	</div>
</div>
