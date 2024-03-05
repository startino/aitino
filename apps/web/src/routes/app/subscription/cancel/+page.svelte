<script lang="ts">
	import * as Card from "$lib/components/ui/card";
	import { Button } from "$lib/components/ui/button";
	import { MoveLeft } from "lucide-svelte";

	export let data;
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
		<Button href="/app"><MoveLeft /> Go Back Home</Button>
	</Card.Footer>
</Card.Root>
