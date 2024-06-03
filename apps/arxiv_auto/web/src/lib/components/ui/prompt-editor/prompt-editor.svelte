<script lang="ts">
	import { Loader2 } from 'lucide-svelte';
	import { PUBLIC_API_URL } from '$env/static/public';

	import * as Dialog from '$lib/components/ui/dialog';
	import { Button } from '$lib/components/ui/button';
	import { Textarea } from '$lib/components/ui/textarea';

	export let value: string;

	let state: 'loading' | 'error' | 'idle' = 'idle';

	const handleSubmit = async () => {
		console.log(value);

		if (!value) {
			return;
		}

		state = 'loading';

		try {
			const wordLimit = 300; // Default to 300 if not provided
			const temperature = 0; // Default to 0 if not provided
			const prompt_type = 'generic'; // Default to generic if not provided

			const apiUrl = `${PUBLIC_API_URL}/improve?word_limit=${wordLimit}&prompt=${encodeURIComponent(value)}&temperature=${temperature}&prompt_type=${prompt_type}`;

			try {
				const response = await fetch(apiUrl);
				if (!response.ok) {
					state = 'error';
					console.log(`request failed: ${response.status}, ${response.statusText}`);
				}

				let data = await response.json();
				console.log(data);
				state = 'idle';
				if (data.startsWith('```markdown')) {
					data = data.substring(11); // Remove the starting ```markdown
					data = data.substring(0, data.lastIndexOf('```')); // Remove the closing ```
				}
				value = data;
			} catch (error) {
				state = 'error';
				console.log(`HTTP error! status: ${error}`);
			}
		} catch (error) {
			state = 'error';
			console.error('Error fetching improved prompt:', error);
		}
	};
</script>

<div>
	<Dialog.Root>
		<Dialog.Trigger class="w-full text-left">
			<div class="grid gap-2">
				{#if value.length > 0}
					<p
						class="line-clamp-2 text-ellipsis rounded-md border border-dashed px-2 py-1 text-gray-400"
					>
						<span class="font-bold text-accent">prompt:</span>
						{value}
					</p>
				{/if}
				<Button class="w-full">Prompt Editor</Button>
			</div>
		</Dialog.Trigger>

		<Dialog.Content class="h-dvh max-w-screen-lg grid-rows-[auto_1fr]">
			<Dialog.Header class="justify-self-center">
				<Button on:click={handleSubmit}>
					Improve prompt with AI

					{#if state === 'loading'}
						<Loader2 class="ml-2 w-4 animate-spin" />
					{/if}
				</Button>
				{#if state === 'error'}
					<span class="text-destructive">Something went please try again...</span>
				{/if}
			</Dialog.Header>
			<Textarea placeholder="Enter you prompt here..." bind:value class="resize-none" />
		</Dialog.Content>
	</Dialog.Root>
</div>
