<script lang="ts">
	import { Plus, XCircle, Loader2 } from 'lucide-svelte';
	import { superForm } from 'sveltekit-superforms';
	import { toast } from 'svelte-sonner';

	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import * as Tabs from '$lib/components/ui/tabs';
	import * as Select from '$lib/components/ui/select';

	export let data;

	const { form, enhance, errors, constraints, submitting } = superForm(data.form, {
		onUpdated: ({ form: f }) => {
			if (f.valid) {
				toast.success(f.message);
			}
		}
	});

	function removeApi(index: number) {
		data.userApiKeys = data.userApiKeys?.filter((_, i) => i !== index);
	}

	$: selectedType = $form.typeId
		? {
				label: data.apiKeyTypes.find((a) => $form.typeId === a.id)?.name as string,
				value: $form.typeId
			}
		: undefined;
</script>

<Tabs.Content value="/app/account/api-keys">
	<Card.Root>
		<Card.Header class="text-xl font-semibold">Your API Keys</Card.Header>
		<Card.Content>
			<form class="mb-6" action="?/add" method="POST" use:enhance>
				{#if $errors._errors}
					<p class="text-red-500">{$errors._errors[0]}</p>
				{/if}
				<div class="flex gap-4">
					<Select.Root
						selected={selectedType}
						onSelectedChange={(v) => {
							v && ($form.typeId = v.value);
						}}
					>
						<Select.Trigger>
							<Select.Value placeholder="API Prodiver" />
						</Select.Trigger>
						<Select.Content>
							{#each data.apiKeyTypes as apiType}
								<Select.Item value={apiType.id}>{apiType.name}</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
					<input hidden name="typeId" bind:value={$form.typeId} />
					<Input
						placeholder="API Value"
						bind:value={$form.value}
						name="value"
						class="focus-visible:ring-1 focus-visible:ring-offset-0"
						{...$constraints.value}
					/>
					<Button type="submit" aria-label="Add API">
						{#if $submitting}
							<Loader2 class="animate-spin" />
						{:else}
							<Plus />
						{/if}
					</Button>
				</div>
				{#if $errors.typeId}
					<p class="text-red-500">{$errors.typeId[0]}</p>
				{/if}
				{#if $errors.value}
					<p class="text-red-500">{$errors.value[0]}</p>
				{/if}
			</form>

			{#if data.userApiKeys.length === 0}
				<p class="text-primary">No API keys added yet.</p>
			{/if}

			<div class="space-y-4">
				{#each data.userApiKeys as api, index (api.id)}
					<form
						action="?/removeAPI&id={api.id}"
						method="POST"
						class="bg-background flex items-center rounded-lg p-4 transition-all duration-300 hover:scale-[99%] hover:shadow-xl"
					>
						<div class="flex">
							<h3 class="mr-1 text-lg font-semibold">{api.api_key_type?.name}</h3>
						</div>
						<Button
							variant="destructive"
							type="submit"
							on:click={() => {
								removeApi(index);
							}}
							class="ml-auto bg-transparent hover:scale-105 hover:bg-transparent"
						>
							<XCircle class="text-destructive hover:scale-105" size="18" />
						</Button>
					</form>
				{/each}
			</div>
		</Card.Content>
	</Card.Root>
</Tabs.Content>
