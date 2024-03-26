<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { MoveLeft } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import { getContext } from '$lib/utils';

	export let data;
	const subStore = getContext('subscriptionStore');
	onMount(async () => {
		$subStore.sub = null;
	});
</script>

<Card.Root class="mx-auto border-destructive">
	<Card.Header>
		<Card.Title>
			<h1 class="text-3xl font-bold">{data.title}</h1>
		</Card.Title>
	</Card.Header>

	<Card.Content>
		{data.message}
	</Card.Content>

	<Card.Footer>
		<Button href="/app"><MoveLeft />Go Back</Button>
	</Card.Footer>
</Card.Root>
