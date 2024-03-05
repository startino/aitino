<script lang="ts">
	import type { PageData } from "./$types";
	import * as Card from "$lib/components/ui/card";
	import { Button } from "$lib/components/ui/button";
	import { MoveRight } from "lucide-svelte";

	export let data: PageData;
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
		<Button href="/app/subscription">Go to your subscription page<MoveRight /></Button>
	</Card.Footer>
</Card.Root>
