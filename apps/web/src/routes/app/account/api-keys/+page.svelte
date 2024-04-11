<script lang="ts">
	import { Plus, Loader2, Trash } from 'lucide-svelte';
	import { superForm } from 'sveltekit-superforms';
	import { toast } from 'svelte-sonner';
	import { fly, slide } from 'svelte/transition';

	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import * as Tabs from '$lib/components/ui/tabs';
	import * as Select from '$lib/components/ui/select';
	import { enhance } from '$app/forms';

	export let data;

	const {
		form,
		enhance: enhanceCreate,
		errors,
		constraints,
		submitting: creating
	} = superForm(data.form, {
		onUpdated: ({ form: f }) => {
			if (f.valid) {
				toast.success(f.message);
			}
		}
	});

	let deleting: string[] = [];

	$: selectedType = $form.typeId
		? {
				label: data.apiKeyTypes.find((a) => $form.typeId === a.id)?.name as string,
				value: $form.typeId
			}
		: { label: 'API Prodiver', value: undefined };
</script>

<Tabs.Content value="/app/account/api-keys">
	<Card.Root>
		<Card.Header class="text-xl font-semibold">Your API Keys</Card.Header>
		<Card.Content>
			<form class="mb-6" action="?/create" method="POST" use:enhanceCreate>
				{#if $errors._errors}
					<p class="text-red-500">{$errors._errors[0]}</p>
				{/if}
				<div class="flex gap-4">
					<Select.Root
						selected={selectedType}
						onSelectedChange={(v) => {
							v?.value && ($form.typeId = v.value);
						}}
					>
						<Select.Trigger class="max-w-xs">
							<Select.Value />
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
						{...$constraints.value}
					/>
					<Button disabled={$creating} type="submit" aria-label="Add API">
						{#if $creating}
							<Loader2 class="animate-spin" />
						{:else}
							<Plus />
						{/if}
					</Button>
				</div>
				{#if $errors.typeId}
					<p class="text-destructive">{$errors.typeId[0]}</p>
				{/if}
				{#if $errors.value}
					<p class="text-destructive">{$errors.value[0]}</p>
				{/if}
			</form>

			{#if data.userApiKeys.filter((api) => !deleting.includes(api.id)).length === 0}
				<p>No API keys</p>
			{/if}

			<ul class="space-y-4">
				{#each data.userApiKeys.filter((api) => !deleting.includes(api.id)) as api (api.id)}
					<li
						in:fly={{ y: 20 }}
						out:slide
						class="bg-background flex items-center justify-between rounded-lg p-4"
					>
						<div class="flex">
							<h3 class="mr-1 text-lg font-semibold">{api.api_key_type?.name}</h3>
						</div>
						<form
							action="?/delete&id={api.id}"
							method="post"
							use:enhance={() => {
								deleting = [...deleting, api.id];
								return async ({ update, result }) => {
									deleting = deleting.filter((id) => id !== api.id);

									if ((result.type = 'failure')) {
										toast.error('Unable to delete the API key...');
										return;
									}
									await update();
								};
							}}
						>
							<button type="submit" disabled={deleting.includes(api.id)}>
								<Trash size={18} />
							</button>
						</form>
					</li>
				{/each}
			</ul>
		</Card.Content>
	</Card.Root>
</Tabs.Content>
