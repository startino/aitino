<script lang="ts">
	import * as AlertDialog from '$lib/components/ui/alert-dialog';
	import { X } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let avatar: string;
</script>

<div
	class="group relative flex aspect-[3/4] flex-col items-center justify-center overflow-hidden rounded-lg bg-surface text-center shadow-md transition-all duration-300 hover:scale-105 hover:shadow-xl"
>
	<!-- TODO: fix the A11y issue without affecting styling -->
	<img
		src={avatar}
		alt={`Entry Avatar`}
		class="flex w-full flex-1 items-center justify-center object-cover object-bottom transition-transform duration-500 group-hover:scale-105"
		on:click={() => {
			dispatch('click');
		}}
	/>
	<div
		class="absolute bottom-0 left-0 right-0 flex flex-grow flex-col border-t border-background/60 bg-black/60 p-4 shadow-inner"
	>
		<slot name="content" />
	</div>
	<!-- delete -->
	<AlertDialog.Root>
		<AlertDialog.Trigger>
			<button
				type="button"
				class="absolute right-4 top-4 z-10 rounded-sm bg-background/60 p-1 text-white transition-all duration-300 disabled:pointer-events-none group-hover:scale-125"
			>
				<div class="transition-all duration-100 hover:scale-125">
					<X />
					<span class="sr-only">Delete</span>
				</div>
			</button>
		</AlertDialog.Trigger>
		<AlertDialog.Content>
			<slot name="delete" />
		</AlertDialog.Content>
	</AlertDialog.Root>
</div>
