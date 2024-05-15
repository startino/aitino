<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog';
	import { Plus } from 'lucide-svelte';
	import { ScrollArea } from '../scroll-area';

	let open = false;
</script>

<Dialog.Root {open}>
	<Dialog.Trigger
		on:click={() => (open = true)}
		class="transition-hover group relative flex aspect-[3/4] flex-col items-center justify-center overflow-hidden rounded-lg border border-primary bg-background from-primary-950 to-primary-800 shadow-lg duration-300 hover:scale-105 hover:bg-gradient-to-br hover:shadow-xl"
	>
		<Plus class="z-10 text-primary transition-all duration-300 group-hover:scale-150 " size="120" />
	</Dialog.Trigger>
	<Dialog.Content class="mt-2 flex h-[calc(100vh-4rem)] w-full flex-col sm:max-w-full lg:max-w-4xl">
		<ScrollArea class="p-4">
			<slot />
		</ScrollArea>
	</Dialog.Content>
</Dialog.Root>
