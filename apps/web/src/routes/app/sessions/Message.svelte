<script lang="ts">
	import { User } from 'lucide-svelte';
	import SvelteMarkdown from 'svelte-markdown';
	import * as models from '$lib/types/models';
	import * as Avatar from '$lib/components/ui/avatar';
	import * as utils from '$lib/utils';

	export let message: models.Message;
	function formatName(inputString: string): string {
		return inputString
			.replace(/([a-z])([A-Z])/g, '$1 $2')
			.replace(/([A-Z])([A-Z][a-z])/g, '$1 $2')
			.replace(/-/g, ' - ');
	}
</script>

<div
	class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg flex max-w-none flex-col items-start justify-end px-12"
>
	<div class="flex w-full justify-center gap-3">
		<Avatar.Root class="h-10 w-10">
			<Avatar.Image src="" />
			<Avatar.Fallback>IMG</Avatar.Fallback>
		</Avatar.Root>

		<div class="flex w-full items-end justify-between gap-4">
			<h2 class="m-0 sm:m-0">{formatName(message.name)}</h2>
			<p class="m-0 sm:m-0">
				{utils.getLocalTime(message.created_at)}
			</p>
		</div>
	</div>
	<SvelteMarkdown source={message.content} />
</div>
