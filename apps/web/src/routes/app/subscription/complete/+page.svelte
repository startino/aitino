<script lang="ts">
	import type { PageData } from './$types';
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { MoveRight } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import { getContext } from '$lib/utils';

	export let data: PageData;
	const subStore = getContext('subscriptionStore');
	onMount(() => {
		$subStore.sub = data.newSub;
		$subStore.tier = data.newTier;
	});
</script>

<Card.Root class="mx-auto">
	<Card.Header>
		<Card.Title>
			<h1 class="text-3xl font-bold">Thank you!</h1>
		</Card.Title>
	</Card.Header>

	<Card.Content>
		<p class="text-primary-500">{data.message}</p>
	</Card.Content>

	<Card.Footer>
		<Button href="/app">Enjoy the App<MoveRight /></Button>
	</Card.Footer>
</Card.Root>
