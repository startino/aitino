<script lang="ts">
	import { fullFormatter, relativeFormatter } from '$lib/utils';
	import { formatDistanceToNowStrict } from 'date-fns';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import { Separator } from '$lib/components/ui/separator';
	import * as Popover from '$lib/components/ui/popover';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import * as Avatar from '$lib/components/ui/avatar';
	import { Switch } from '$lib/components/ui/switch';
	import { Label } from '$lib/components/ui/label';
	import { Textarea } from '$lib/components/ui/textarea';
	import { Input } from '$lib/components/ui/input';
	import { Calendar } from '$lib/components/ui/calendar';
	import * as Dialog from '$lib/components/ui/dialog';
	import {
		Archive,
		ArchiveX,
		Trash2,
		Clock,
		Reply,
		ReplyAll,
		Forward,
		EllipsisVertical
	} from 'lucide-svelte';
	import type { Lead } from '$lib/types';
	import * as api from '$lib/api';
	import type { UUID } from '$lib/types';

	export let lead: Lead;

	let url: string;
	$: url = lead.data?.url ?? '';
	let subreddit: string;
	$: subreddit = extractSubreddit(url);

	function extractSubreddit(url: string): string {
		// Parse the URL
		const parsedUrl = new URL(url);

		// Extract the pathname
		const pathname = parsedUrl.pathname;

		// Extract the subreddit name
		const parts = pathname.split('/');
		const subreddit = 'r/' + parts[2]; // Assuming the subreddit name is always the second component

		return subreddit;
	}

	let reasonTextValue = 'Post is irrelevant because';
	let commentTextValue = lead.comment ?? '';

	async function handlePublishComment() {
		console.log('Trying to publish');
		const res: boolean = await api.publishComment(lead.id, lead.comment);
		if (res) {
			console.log('Comment published');
		} else {
			console.log('Comment not published');
		}
	}

	async function handleIrrelevant() {
		console.log('Trying to mark as irrelevant');
		const res: boolean = await api.markAsIrrelevant(lead.id, lead.submission_id, reasonTextValue);
		if (res) {
			console.log('Marked as irrelevant');
			// Reactive UI management to show lead was removed
			lead.data!.body = '';

			reasonTextValue = 'Post is irrelevant because';
		} else {
			console.log('Not marked as irrelevant');
		}
	}

	async function handleGenerateComment() {
		console.log('Trying to generate comment');
		const comment: string = await api.generateComment(lead.data?.title, lead.data?.body);
		if (comment != '') {
			console.log('Comment generated');
			commentTextValue = comment;
		} else {
			console.log('Comment not generated');
		}
	}
</script>

<div class="flex h-full flex-col">
	{#if lead}
		<div class="flex h-full flex-1 flex-col overflow-hidden text-left">
			<div class="flex items-start p-4">
				<h1 class="bold text-2xl">{lead.data?.title}</h1>
				{#if lead.discovered_at}
					<div class="ml-auto text-sm text-muted-foreground">
						Posted {formatDistanceToNowStrict(lead.discovered_at, { addSuffix: true })}
					</div>
				{/if}
			</div>
			<div class="flex flex-col gap-2 p-4">
				<h3>{subreddit}</h3>
				<a href={url} class="text-accent underline">See post</a>
			</div>
			<Separator />
			<div class="flex-1 overflow-y-auto whitespace-pre-wrap p-4 text-left text-sm">
				<p class="text-md tracking-widest">{lead.data.body}</p>
			</div>
			<Separator class="mt-auto" />
			<div class="p-4">
				<form>
					<div class="grid gap-4">
						<Textarea
							class="h-64 p-4"
							placeholder={`Reply ${lead.id}...`}
							bind:value={lead.comment}

						/>
						<div class="flex items-center">
							{#if lead.status == 'under_review'}
								<Dialog.Root>
									<Dialog.Trigger class={buttonVariants({ variant: 'destructive' })}
										>Irrelevant</Dialog.Trigger
									>
									<Dialog.Content class="sm:max-w-[425px]">
										<Dialog.Header>
											<Dialog.Title>Mark as irrelevant</Dialog.Title>
											<Dialog.Description>
												You think this post is a false positive and irrelevant. Please provide a
												reason.
											</Dialog.Description>
										</Dialog.Header>
										<Textarea
											class="w-full"
											placeholder="Post is irrelevant because ..."
											bind:value={reasonTextValue}
										/>
										<Dialog.Footer>
											<Button
												type="submit"
												on:click={() => {
													handleIrrelevant();
												}}>Submit</Button
											>
										</Dialog.Footer>
									</Dialog.Content>
								</Dialog.Root>
								<div class="ml-auto flex flex-row gap-4">
									<Button on:click={() => handleGenerateComment()} variant="secondary"
										>Generate new comment</Button
									>
									<Button
										class=""
										on:click={() => {
											handlePublishComment();
										}}>Publish</Button
									>
								</div>
							{/if}
						</div>
					</div>
				</form>
			</div>
		</div>
	{:else}
		<div class="p-8 text-center text-muted-foreground">No lead selected</div>
	{/if}
</div>
