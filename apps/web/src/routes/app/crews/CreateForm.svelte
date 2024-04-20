<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { createCrewSchema, type CreateCrewSchema } from '$lib/schema';
	import { superForm, type Infer, type SuperValidated } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let formCreate: SuperValidated<Infer<CreateCrewSchema>>;

	const form = superForm(formCreate, {
		validators: zodClient(createCrewSchema)
	});

	const { form: formData, enhance } = form;
</script>

<form method="POST" use:enhance>
	<Form.Field {form} name="title">
		<Form.Control let:attrs>
			<Form.Label>Title</Form.Label>
			<Input {...attrs} bind:value={$formData.title} />
		</Form.Control>
		<Form.Description>This is the title of the crew.</Form.Description>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Button>Create</Form.Button>
</form>
