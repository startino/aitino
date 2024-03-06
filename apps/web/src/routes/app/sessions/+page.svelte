<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import Chat from './Chat.svelte';
	import { onMount } from 'svelte';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { error } from '@sveltejs/kit';
	import type { Message, Session } from '$lib/types/models';
	import { get, writable } from 'svelte/store';
	import type { PageData } from './$types';
	import * as Sheet from '$lib/components/ui/sheet';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import * as utils from '$lib/utils';
	import * as Popover from '$lib/components/ui/popover';
	import {
		ArrowLeftFromLine,
		ArrowLeftToLine,
		ArrowRightToLine,
		CheckCircle,
		Loader,
		Loader2,
		MoreHorizontal
	} from 'lucide-svelte';
	import { Description } from '$lib/components/ui/alert';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { supabase } from '$lib/supabase';

	export let data: PageData;

	let { recentSession, allSessions, recentCrew, sessionMessages, newSession } = data;

	let activeSession = recentSession;
	let messages: Message[] = sessionMessages;

	// Reactivity for the Crew chat
	let loadingSession = true;
	let loadingMessages = true;
	let waitingforUser = false;

	// Reactivity for renaming
	let renamePopoverOpen = false;
	let renamingSession = '';
	let renamingValue = '';
	let renamingInProgress = false;

	// Reactivity for deleting
	let deletingInProgress = false;
	let deletingSession = '';

	// Helper function to reset the UI after renaming or if its cancelled
	function resetRenamingUI() {
		renamePopoverOpen = false;
		renamingInProgress = false;
		renamingSession = '';
		renamingValue = '';
	}

	function resetDeletingUI() {
		deletingInProgress = false;
		deletingSession = '';
	}

	async function renameSession(sessionId: string) {
		// If multiple queues to submit the rename request, ignore the rest.
		if (renamingInProgress) {
			return;
		}

		const currentTitle = (await allSessions).find((session) => session.id === sessionId);

		// If no session is being renamed, ignore
		if (!activeSession) {
			resetRenamingUI();
			return;
		}
		// If no changes were made, reset the UI and ignore
		if (activeSession?.title == renamingValue) {
			resetRenamingUI();
			return;
		}

		renamingInProgress = true;
		console.log('renaming', renamingValue, sessionId);
		const response = await fetch(`?/rename`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, newTitle: renamingValue })
		});
		const data = await response.json();
		// Update the session locally in order to not refetch
		const localVariable = await allSessions;
		allSessions = localVariable.map((session) => {
			if (session.id === sessionId) {
				session.title = renamingValue;
			}
			return session as Session;
		});
		// Reset the renaming variables
		resetRenamingUI();
	}

	async function deleteSession(sessionId: string) {
		deletingInProgress = true;
		deletingSession = sessionId;
		const response = await fetch(`?/delete`, {
			method: 'POST',
			body: JSON.stringify({ sessionId })
		});
		const data = await response.json();
		// Update the session locally in order to not refetch
		const localSessions = await allSessions;
		allSessions = localSessions.filter((session) => session.id !== sessionId);
		resetDeletingUI();

		if (activeSession?.id === sessionId) {
			activeSession = null;
			messages = [];
		}
	}

	onMount(async () => {
		if (newSession.crewId && newSession.title) {
			startNewSession(newSession.crewId, newSession.title);
		}
	});

	async function startNewSession(crewId: string, title: string) {
		console.log('Starting new session...');
		// Reset the UI and local variables
		activeSession = null;
		messages = [];
		loadingSession = true;

		// Instantiate and get the new session
		const res = await fetch(
			`${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${data.session?.user.id}&title=${title}`
		);
		const result = await res.json();
		if (result.succ)
		console.log('result: ', result);
		const sessionId = result.sessionId;

		// Set it up locally
		const sessionResponse = await fetch(`?/get-session?sessionId=${sessionId}`);
		const session = await sessionResponse.json();
		activeSession = session;

		loadingSession = false;
	}

	async function loadSession(sessionId: string) {
		loadingSession = true;
		let sessionResponse = await fetch(`?/get-session?sessionId=${sessionId}`);
		activeSession = await sessionResponse.json();
		loadingSession = false;
		loadingMessages = true;
		let messageResponse = await fetch(`?/get-messages?sessionId=${sessionId}`);
		messages = await messageResponse.json();
		loadingMessages = false;
	}

	async function loadMessage(sessionId: string) {
		const res = await fetch(`?/get-session?sessionId=${sessionId}`);
		const data = await res.json();
		const session = data.session;
	}

	function redirectToCrewEditor() {
		window.location.href = '/app/editor/crew';
	}
</script>

<div class="flex h-full flex-row place-items-center">
	<div class="flex h-full w-full">
		{#if !activeSession}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto mt-auto flex h-full max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>Loading the session...</h1>
			</div>
			{#if recentCrew}
				<div
					class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
				>
					<h1>It looks like you don't have session yet...</h1>
					{#await recentCrew}
						<p>Loading...</p>
					{:then recentCrew}
						<Button on:click={() => startNewSession(recentCrew.id, 'New Session')}
							>Run Your Crew!</Button
						>
					{:catch}
						<p>Failed to load crew</p>
					{/await}
				</div>
			{/if}
		{:else}
			<Chat
				session={activeSession}
				name={activeSession?.title}
				{messages}
				waitingForUser={waitingforUser}
			/>
		{/if}
	</div>
	<Sheet.Root onOutsideClick={() => renameSession(renamingSession)}>
		<Sheet.Trigger asChild let:builder>
			<Button builders={[builder]} class="my-auto mr-8 h-14 w-14">
				<ArrowLeftFromLine size="24" />
			</Button>
		</Sheet.Trigger>
		<Sheet.Content side="right">
			<Sheet.Header>
				<Sheet.Description>
					{#if activeSession}
						Click anywhere on the left to continue with your most recent session
					{/if}
				</Sheet.Description>
			</Sheet.Header>

			<Sheet.Footer class="mt-2">
				<Sheet.Close asChild let:builder>
					<div class="flex h-full w-full flex-col gap-2">
						{#if recentCrew}
							<Button
								class="mb-2 w-full"
								builders={[builder]}
								on:click={() => startNewSession(recentCrew.id, 'New Session from Button')}
								>Start New Session</Button
							>
						{/if}
						<ul class="flex w-full flex-col gap-2">
							{#await allSessions}
								<p>Loading...</p>
							{:then allSessions}
								{#each allSessions as session}
									<li class="flex w-full flex-row gap-2">
										{#if renamePopoverOpen && renamingSession === session.id}
											<Input
												type="text"
												class="-ml-4 w-full"
												placeholder={session.title ?? 'Empty'}
												disabled={renamingInProgress}
												on:focusout={() => renameSession(session.id)}
												on:keydown={(e) => {
													if (e.key === 'Enter') {
														renameSession(session.id);
													}
												}}
												bind:value={renamingValue}
											/>
											<Button
												type="submit"
												disabled={renamingInProgress}
												on:click={() => {
													() => renameSession(session.id);
												}}
											>
												{#if renamingInProgress}
													<Loader size="18" />
												{:else}
													<CheckCircle size="18" />
												{/if}
											</Button>
										{:else}
											<Button
												builders={[builder]}
												variant="outline"
												class="flex w-full flex-row justify-between {activeSession?.id == session.id
													? 'bg-accent text-accent-foreground'
													: 'hover:bg-accent/20 hover:text-foreground'}"
												on:click={() => loadSession(session.id)}
											>
												{session.title}
												<div class="text-foreground/75 text-right text-xs">
													Last opened {utils.daysRelativeToToday(session.created_at).toLowerCase()}
												</div>
											</Button>
										{/if}
										<DropdownMenu.Root>
											<DropdownMenu.Trigger asChild let:builder>
												<Button
													builders={[builder]}
													disabled={deletingSession === session.id}
													variant="icon"
													class="aspect-square h-full"
												>
													{#if deletingInProgress && deletingSession === session.id}
														<Loader size="18" class="mx-auto my-auto " />
													{:else}
														<MoreHorizontal size="18" />
													{/if}
												</Button>
											</DropdownMenu.Trigger>

											<DropdownMenu.Content class="w-56">
												<DropdownMenu.Group>
													<DropdownMenu.Item
														on:click={() => {
															renamePopoverOpen = true;
															renamingSession = session.id;
														}}
													>
														Rename
														<DropdownMenu.Shortcut>r</DropdownMenu.Shortcut>
													</DropdownMenu.Item>
												</DropdownMenu.Group>
												<DropdownMenu.Separator />
												<DropdownMenu.Group>
													<DropdownMenu.Item on:click={() => deleteSession(session.id)}>
														Delete
														<DropdownMenu.Shortcut>d</DropdownMenu.Shortcut>
													</DropdownMenu.Item>
												</DropdownMenu.Group>
											</DropdownMenu.Content>
										</DropdownMenu.Root>
									</li>
								{/each}
							{/await}
						</ul>
					</div>
				</Sheet.Close>
			</Sheet.Footer>
		</Sheet.Content>
	</Sheet.Root>
</div>
