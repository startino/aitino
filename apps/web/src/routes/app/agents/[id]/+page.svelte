<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { agentSchema } from '$lib/schema';
	import { fail, superForm, superValidate } from 'sveltekit-superforms';
	import { zod, zodClient } from 'sveltekit-superforms/adapters';
	import * as Form from '$lib/components/ui/form';
	import * as Select from '$lib/components/ui/select';
	import api from '$lib/api';
	import { goto } from '$app/navigation';

	export let data;

	let { agent, form: formUpdate } = data;

	const form = superForm(formUpdate, {
		validators: zodClient(agentSchema)
	});

	const { form: formData } = form;

	$formData = {
		id: agent.id,
		title: agent.title,
		description: agent.description ?? '',
		published: agent.published,
		tools: [],
		model: agent.model,
		role: agent.role,
		system_message: agent.system_message
	};

	$: selectedModel = $formData.model
		? {
				label: $formData.model,
				value: $formData.model
			}
		: undefined;

	const updateAgent = async (request: any) => {
		console.log('update agent');

		const _form = await superValidate(request, zod(agentSchema));

		if (!_form.valid) {
			return fail(400, { form: _form, message: 'unable to create a new agent' });
		}

		const agent = await api
			.PATCH('/agents/{id}', {
				params: {
					path: {
						id: _form.data.id
					}
				},
				body: {
					title: _form.data.title,
					description: _form.data.description,
					published: _form.data.published,
					role: _form.data.role,
					tools: [],
					system_message: _form.data.system_message,
					model: _form.data.model
				}
			})
			.then(({ data: d, error: e }) => {
				if (e) {
					console.error(`Error creating crew: ${e.detail}`);
					return null;
				}
				if (!d) {
					console.error(`No data returned from crew creation`);
					return null;
				}
				return d;
			});

		if (!agent) {
			return fail(500, {
				form: _form,
				message: 'Agent update failed. Please try again. If the problem persists, contact support.'
			});
		}

		goto(`/app/agents`);
	};
</script>

<form
	class="flex w-full flex-col items-center justify-center gap-4 p-4"
	on:submit={() => updateAgent($formData)}
>
	<div class="flex flex-col gap-4">
		<div class="flex gap-4">
			<div class="flex w-full flex-1 flex-col gap-4">
				<h2 class="text-xl">Updating Agent</h2>
				<p class="opacity-70">You are about to update an Agent. Please fill out the form below.</p>

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
			</div>
			<div
				class="relative flex aspect-[3/4] h-96 flex-col items-center justify-center overflow-hidden rounded-lg bg-surface text-center shadow-md"
			>
				<img
					src={agent.avatar}
					alt={`Agent Avatar`}
					class="flex w-full flex-1 items-center justify-center object-cover object-bottom"
				/>
			</div>
		</div>

		<h3 class="pt-4 text-lg">Functional Options</h3>
		<Form.Field {form} name="model">
			<Form.Control let:attrs>
				<Form.Label>Model*</Form.Label>
				<Select.Root
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
	</div>
</form>
