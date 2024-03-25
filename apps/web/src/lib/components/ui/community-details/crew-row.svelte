<script lang="ts">
	import type { Crew } from '$lib/types/models';
	import { fade } from 'svelte/transition';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let crew: Crew;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	class="cursor-pointer hover:scale-[101%]"
	transition:fade={{ delay: 500, duration: 400 }}
	on:click={() => dispatch('click', { id: crew.id })}
>
	<Card.Root>
		<div class="flex items-center justify-between px-6">
			<div class="flex gap-4 gap-y-4 p-4">
				<div class="flex h-20 w-20 items-center justify-center rounded-full bg-primary-200 p-1">
					<img
						src={crew.avatar}
						alt={crew.title}
						class="rounded-full border-4 object-cover shadow-2xl"
					/>
				</div>
				<div class="flex flex-col">
					<div
						class="bg-gradient-to-r from-green-200 to-teal-300 bg-clip-text text-2xl font-extrabold text-transparent"
					>
						{crew.title}
					</div>
				</div>
			</div>
			<div class="flex h-full items-center justify-between">
				<Button variant="ghost" class="max-w-xs px-12  text-foreground hover:bg-transparent"
					>see more</Button
				>
				<button
					class="inline-flex h-10 max-w-xs items-center justify-center whitespace-nowrap rounded-md bg-primary px-12 py-2 text-sm font-bold text-primary-foreground ring-offset-background transition-colors hover:scale-[98%] hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
					on:click|stopPropagation={() => dispatch('load', crew)}>Load</button
				>
			</div>
		</div>
		<Card.Content>
			<div class="flex items-center justify-between px-0">
				<p class="max-w-4xl px-6">
					{crew.description}
				</p>
			</div>
		</Card.Content>
	</Card.Root>
</div>
