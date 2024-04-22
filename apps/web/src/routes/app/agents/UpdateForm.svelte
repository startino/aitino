<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { agentSchema, type AgentSchema } from '$lib/schema';
	import { superForm, type Infer, type SuperValidated } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import * as Form from '$lib/components/ui/form';
	import * as Select from '$lib/components/ui/select';
	import * as Dialog from '$lib/components/ui/dialog';
	import type { schemas } from '$lib/api';

	export let formUpdate: SuperValidated<Infer<AgentSchema>>;
	export let agent: schemas['Agent'];

	const form = superForm(formUpdate, {
		validators: zodClient(agentSchema)
	});

	$: selectedModel = $formData.model
		? {
				label: $formData.model,
				value: $formData.model
			}
		: undefined;

	const { form: formData, enhance } = form;

	$formData = {
		title: agent.title,
		description: agent.description ?? '',
		published: agent.published,
		tools: agent.tools,
		model: agent.model === 1 ? 'gpt-4-turbo' : 'gpt-3.5-turbo',
		role: agent.role,
		system_message: agent.system_message
	};
</script>

<form class="flex flex-col gap-4" method="POST" action="?/update" use:enhance>
	<Dialog.Header>
		<Dialog.Title>Update a new Agent</Dialog.Title>
		<Dialog.Description>
			You are about to update an Agent. Please fill out the form below.
		</Dialog.Description>
	</Dialog.Header>
	<h3 class="pt-4 text-lg">Basic Information</h3>
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

	<h3 class="pt-4 text-lg">Functional Options</h3>
	<Form.Field {form} name="model">
		<Form.Control let:attrs>
			<Form.Label>Model*</Form.Label>
			<Select.Root
				{...attrs}
				selected={selectedModel}
				onSelectedChange={(v) => {
					v && ($formData.model = v.value);
				}}
			>
				<Select.Trigger>
					<Select.Value placeholder="Select a Model" />
				</Select.Trigger>
				<Select.Content>
					<Select.Group>
						<Select.Label>Models</Select.Label>
						<Select.Item value="gpt-4-turbo" label="gpt-4-turbo">gpt-4-turbo</Select.Item>
						<Select.Item value="gpt-3.5-turbo" label="gpt-3.5-turbo">gpt-3.5-turbo</Select.Item>
					</Select.Group>
				</Select.Content>
			</Select.Root>
		</Form.Control>
	</Form.Field>
	<Form.Field {form} name="role">
		<Form.Control let:attrs>
			<Form.Label>Role*</Form.Label>
			<Input {...attrs} bind:value={$formData.role} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="system_message">
		<Form.Control let:attrs>
			<Form.Label>System Message*</Form.Label>
			<Textarea class="w-full" {...attrs} bind:value={$formData.system_message} />
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>

	<p class="text-sm opacity-50">* required fields</p>
	<Form.Button>Update</Form.Button>
</form>
