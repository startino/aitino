<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { createCrewSchema, type CreateCrewSchema } from '$lib/schema';
	import { superForm, type Infer, type SuperValidated } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let formCreate: SuperValidated<Infer<CreateCrewSchema>>;

	const form = superForm(formCreate, {
		validators: zodClient(createCrewSchema)
	});

	const { form: formData, enhance } = form;
</script>

<form class="flex flex-col gap-4" method="POST" action="?/create" use:enhance>
	<h2>Create a new Crew</h2>
	<Form.Field {form} name="title">
		<Form.Control let:attrs>
			<Form.Label>Title*</Form.Label>
			<Input {...attrs} bind:value={$formData.title} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="description">
		<Form.Control let:attrs>
			<Form.Label>Description</Form.Label>
			<Textarea class="w-full" {...attrs} bind:value={$formData.description} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="published">
		<Form.Control let:attrs>
			<Form.Label>Publish</Form.Label>
			<Checkbox {...attrs} bind:checked={$formData.published} />
		</Form.Control>
		<Form.Description class="inline">Check this to publish the crew.</Form.Description>
		<Form.FieldErrors />
	</Form.Field>

	<p class="text-sm opacity-50">* required fields</p>
	<Form.Button>Create</Form.Button>
</form>
