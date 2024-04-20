<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Plus } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let open = false;
	const handleTrigger = async () => {
		open = true;
	};
</script>

<Dialog.Root {open} onOpenChange={(o) => dispatch('close')}>
	<Dialog.Trigger
		on:click={handleTrigger}
		class="transition-hover group relative flex aspect-[3/4] flex-col items-center justify-center overflow-hidden rounded-lg bg-background from-primary-950 to-primary-800 shadow-lg duration-1000 hover:scale-105 hover:bg-gradient-to-br hover:shadow-xl"
	>
		<Plus class="z-10 transition-all duration-300 " size="120" />
	</Dialog.Trigger>
	<Dialog.Content class="w-full sm:max-w-full lg:max-w-4xl">
		<slot />
	</Dialog.Content>
</Dialog.Root>
