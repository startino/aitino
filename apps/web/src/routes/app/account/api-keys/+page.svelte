<script lang="ts">
	import { Plus, XCircle } from 'lucide-svelte';

	import * as Card from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { browser } from '$app/environment';
	import * as Tabs from '$lib/components/ui/tabs';
	import { enhance } from '$app/forms';
	import * as Select from '$lib/components/ui/select';

	export let data;
	let newApiValue = '';

	let inputs: { name: string; value: string }[] = [];

	$: apiTypes = data.apiKeyTypes;

	$: myApi = data.userApiKeys;

	$: {
		if (browser && inputs.length > 0) {
			const inputMap = inputs.reduce((prev, curr) => {
				if (!curr.name) return prev;
				return {
					...prev,
					[curr.name.trim()]: curr.value
				};
			}, {});

			localStorage.setItem('premade-inputs', JSON.stringify(inputMap));
		}
	}

	function removeApi(index: number) {
		myApi = myApi?.filter((_, i) => i !== index);
	}

	$: apiId = null;
</script>

<Tabs.Content value="/app/account/api-keys">
	<Card.Root>
		<Card.Header class="text-xl font-semibold">Your API Keys</Card.Header>
		<Card.Content>
			<form
				class="mb-6"
				action="?/addAPI&id={apiId !== undefined ? apiId : ''}"
				method="POST"
				use:enhance
			>
				<div class="flex gap-4">
					<Select.Root>
						<Select.Trigger>
							<Select.Value placeholder="API Prodiver" />
						</Select.Trigger>
						<Select.Content>
							{#each apiTypes as apiType}
								<Select.Item value={apiType.name}>
									{apiType.name}
								</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
					<Input
						placeholder="API Value"
						bind:value={newApiValue}
						name="apiValue"
						class="focus-visible:ring-1 focus-visible:ring-offset-0"
					/>
					<Button type="submit" class="shrink-0">
						<Plus class="mr-2" /> Add API
					</Button>
				</div>
			</form>

			{#if myApi.length === 0}
				<p class="text-primary">No API keys added yet.</p>
			{/if}

			<div class="space-y-4">
				{#each myApi as api, index}
					<form
						action="?/removeAPI&id={api.id}"
						method="POST"
						use:enhance
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
