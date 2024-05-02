<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
</script>

<Card.Root>
	<Card.Header>
		<Card.Title class="text-2xl">Check Your Email</Card.Title>
	</Card.Header>
	<Card.Content>
		<p>
			We've sent a confirmation email to you. Please check your inbox to complete the registration
			process.
		</p>
		<Button href="/auth" class="mt-4">Go to Login</Button>
	</Card.Content>
</Card.Root>
