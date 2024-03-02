<script lang="ts">
	import { User } from "lucide-svelte";
	import SvelteMarkdown from "svelte-markdown";
	import * as models from "$lib/types/models";
	export let message: models.Message;
	function formatName(inputString: string): string {
		return inputString
			.replace(/([a-z])([A-Z])/g, "$1 $2")
			.replace(/([A-Z])([A-Z][a-z])/g, "$1 $2")
			.replace(/-/g, " - ");
	}
</script>

<div
	class="xl:prose-md prose prose-sm prose-main flex max-w-none flex-col items-start justify-end px-12 md:prose-base 2xl:prose-lg"
>
	<div class="flex w-full justify-center gap-3">
		<User size="36" class="ml-[-2.6em]" />
		<div class="flex w-full items-end justify-between gap-4">
			<h2 class="m-0 sm:m-0">{formatName(message.name)}</h2>
			<p class="m-0 sm:m-0">
				{message.created_at.toString().split(".")[0]}
			</p>
		</div>
	</div>
	<SvelteMarkdown source={message.content} />
</div>
