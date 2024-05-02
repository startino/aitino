<script lang="ts">
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { emailAuthSchema, type EmailAuthSchema } from '$lib/schema';
	import { superForm, type Infer, type SuperValidated } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';

	export let formRegister: SuperValidated<Infer<EmailAuthSchema>>;

	const form = superForm(formRegister, {
		validators: zodClient(emailAuthSchema)
	});

	const { form: formData } = form;
</script>

<form
	class="items-between flex w-full flex-col justify-center gap-4"
	method="POST"
	action="?/authEmail"
>
	<Form.Field {form} name="email">
		<Form.Control let:attrs>
			<Form.Label>E-Mail</Form.Label>
			<Input {...attrs} bind:value={$formData.email} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<Form.Button>Submit</Form.Button>
</form>
