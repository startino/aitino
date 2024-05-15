<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { Switch } from '$lib/components/ui/switch';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Loader2 } from 'lucide-svelte';
	import { enhance } from '$app/forms';

	export let open = false;
</script>

<Dialog.Root {open} onOpenChange={(o) => (open = o)}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Edit crew</Dialog.Title>
		</Dialog.Header>

		<form class="p-4" action="?/edit" method="POST" use:enhance>
			<div class="mb-2 flex w-full items-center gap-2">
				<!-- <div class="w-full space-y-4"> -->
				<!-- 	<Label for="title" class="text-right">Title</Label> -->
				<!-- 	<input bind:value={$form.id} name="id" hidden /> -->
				<!-- 	<Input -->
				<!-- 		name="title" -->
				<!-- 		bind:value={$form.title} -->
				<!-- 		class="col-span-3 focus-visible:ring-1 focus-visible:ring-offset-0" -->
				<!-- 	/> -->
				<!-- </div> -->
				<div class="mt-8 flex items-center space-x-2">
					<Label for="published" class="flex items-center">
						<!-- <Switch id="published" name="published" bind:checked={$form.published} /> -->
						<span class="ml-2 text-sm text-gray-700">Published</span>
					</Label>
				</div>
			</div>
			<!-- {#if $errors.title} -->
			<!-- 	<p class="text-red-500">{$errors.title[0]}</p> -->
			<!-- {/if} -->
			<div class="mb-2 flex w-full items-center gap-2">
				<div class="w-full space-y-4">
					<Label for="description" class="text-right">Description</Label>
					<!-- <Textarea -->
					<!-- 	id="description" -->
					<!-- 	name="description" -->
					<!-- 	bind:value={$form.description} -->
					<!-- 	class="block h-24 w-full resize-none focus-visible:ring-1 focus-visible:ring-offset-0 [&::-webkit-scrollbar]:hidden" -->
					<!-- ></Textarea> -->
				</div>
			</div>
			<!-- {#if $errors.description} -->
			<!-- 	<p class="text-red-500">{$errors.description[0]}</p> -->
			<!-- {/if} -->
			<!-- {#if $errors._errors} -->
			<!-- 	<p class="text-red-500">{$errors._errors[0]}</p> -->
			<!-- {/if} -->
			<Dialog.Footer>
				<Button type="submit">
					<!-- {#if state === 'loading'} -->
					<!-- 	<Loader2 class="mr-2 mt-1 h-4 w-4 animate-spin" /> -->
					<!-- {/if} -->
					Save changes
				</Button>
			</Dialog.Footer>
		</form></Dialog.Content
	>
</Dialog.Root>
