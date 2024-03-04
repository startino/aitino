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
		MoreHorizontal
	} from 'lucide-svelte';
	import { Description } from '$lib/components/ui/alert';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';

	export let data: PageData;

	let { recentSession, allSessions, recentCrew, recentSessionMessages } = data;

	let loadingSession = true;
	let loadingMessages = true;
	let awaitingReply = false;

	let activeSession = recentSession;
	let messages: Message[] | Promise<Message[]> = recentSessionMessages;

	// Reactivity
	let rightSideBarOpen = true;
	let renamePopoverOpen = false;
	let renamingItem = -1;
	let renamingValue = '';
	let renamingInProgress = false;

	// Helper function to reset the UI after renaming or if its cancelled
	function resetRenamingUI() {
		renamingInProgress = false;
		renamingItem = -1;
		renamingValue = '';
	}

	async function renameSession(sessionId: string) {
		const currentName = (await allSessions).find((session) => session.id === sessionId);
		if (!currentName) {
			resetRenamingUI();
			return;
		}
		if (currentName?.name == renamingValue) {
			resetRenamingUI();
			return;
		}

		renamingInProgress = true;
		const response = await fetch(`?/rename`, {
			method: 'POST',
			body: JSON.stringify({ sessionId, newName: renamingValue })
		});
		const data = await response.json();
		// Update the session locally in order to not refetch
		const localVariable = await allSessions;
		allSessions = localVariable.map((session) => {
			if (session.id === sessionId) {
				session.name = renamingValue;
			}
			return session as Session;
		});
		// Reset the renaming variables
		renamingInProgress = false;
		renamingItem = -1;
		renamingValue = '';
		console.log('rename', renamingValue);
	}

	onMount(async () => {
		loadingSession = false;
	});

	async function* callCrew(url: string): AsyncGenerator<string, void, unknown> {
		const response = await fetch(url);
		const reader = response.body?.getReader();

		if (!reader) {
			throw new Error('Invalid response');
		}

		while (true) {
			const { done, value } = await reader.read();

			if (done) {
				break;
			}

			const line = new TextDecoder().decode(value);

			if (!line) {
				break;
			}

			yield line;
		}
	}

	async function main(url: string): Promise<void> {
		if (!url) {
			console.log('Usage: Provide a valid URL as a parameter');
			return;
		}

		for await (const event of callCrew(url)) {
			let e = null;
			try {
				e = JSON.parse(event.trim());
				console.log('got message', e);
			} catch (error) {
				console.error(`Error parsing JSON ${error}:`, event);
				continue;
			}
			if (!e) {
				continue;
			}

			if (e.id === 0) {
				activeSession = {
					name: e.data.name,
					id: e.data.session_id,
					crew_id: e.data.maeva_id,
					profile_id: e.data.profile_id,
					created_at: e.data.created_at
				};
				loadingSession = false;
				console.log('got session id', e.data.session_id);
				continue;
			}
			if (e.data === 'done') {
				awaitingReply = true;
				console.log('done');

				return;
			}

			messages = [...(await messages), e.data];
		}
	}

	function startNewSession(crewId: string) {
		activeSession = null;
		messages = [];
		loadingSession = true;

		const url = `${PUBLIC_API_URL}/crew?id=${crewId}&profile_id=${data.session.user.id}`;

		main(url);
	}

	async function loadSession(sessionId: string, crewId: string) {
		loadingSession = true;
		let sessionResponse = await fetch(`?/get-session?sessionId=${sessionId}&crewId=${crewId}`);
		activeSession = await sessionResponse.json();
		loadingSession = false;
		loadingMessages = true;
		let messageResponse = await fetch(`?/get-messages?sessionId=${sessionId}`);
		messages = await messageResponse.json();
		loadingMessages = false;
	}

	function replySession(message: string) {
		if (!activeSession) {
			throw error(500, 'Cannot reply without session');
		}
		awaitingReply = false;
		const url = `${PUBLIC_API_URL}/crew?id=${activeSession.crew_id}&profile_id=${activeSession.profile_id}&session_id=${activeSession.id}&reply=${message}`;

		main(url);
	}

	function redirectToCrewEditor() {
		window.location.href = '/app/editor/crew';
	}
</script>

<main class="flex flex-row">
	<div class="w-full">
		{#if loadingSession}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>Loading...</h1>
			</div>
		{:else if activeSession}
			<Chat
				sessionId={activeSession?.id}
				name={activeSession?.name}
				{messages}
				{awaitingReply}
				replyCallback={replySession}
			/>
		{:else if recentCrew}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>It looks like you don't have session yet...</h1>
				{#await recentCrew}
					<p>Loading...</p>
				{:then recentCrew}
					<Button on:click={() => startNewSession(recentCrew.id)}>Run Your Crew!</Button>
				{:catch}
					<p>Failed to load crew</p>
				{/await}
			</div>
		{:else}
			<div
				class="xl:prose-md prose prose-sm prose-main md:prose-base 2xl:prose-lg mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center"
			>
				<h1>It looks like you haven't created a crew yet...</h1>
				<Button on:click={redirectToCrewEditor}>Go Create One!</Button>
			</div>
		{/if}
		<div class="absolute bottom-1 mx-auto flex h-min w-fit flex-col items-center justify-center">
			<code class="text-muted">debug:</code>
			<code class="text-muted">
				crew id: {recentCrew?.id ?? 'missing'} - session id: {activeSession?.session?.id ??
					'missing'}
			</code>
		</div>
	</div>
	<Sheet.Root onOutsideClick={() => resetRenamingUI()}>
		<Sheet.Trigger asChild let:builder>
			<Button builders={[builder]} class="h-14 w-14">
				{#if rightSideBarOpen}
					<ArrowRightToLine size="24" />
				{:else}
					<ArrowLeftFromLine size="24" />
				{/if}
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
								on:click={() => startNewSession(recentCrew.id)}>Start New Session</Button
							>
						{/if}
						<ul class="flex w-full flex-col gap-2">
							{#await allSessions}
								<p>Loading...</p>
							{:then allSessions}
								{#each allSessions as session, i}
									<li class="flex w-full flex-row gap-2">
										{#if renamePopoverOpen && renamingItem === i}
											<Input
												type="text"
												class="-ml-4 w-full"
												placeholder={session.name ?? 'Unamed'}
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
												on:click={() => loadSession(session.id, session.crew_id)}
											>
												{session.name}
												<div class="text-right">
													Last opened {utils.daysRelativeToToday(session.created_at)}
												</div>
											</Button>
										{/if}
										<DropdownMenu.Root>
											<DropdownMenu.Trigger asChild let:builder>
												<Button builders={[builder]} variant="icon" class="aspect-square h-full"
													><MoreHorizontal size="18" /></Button
												>
											</DropdownMenu.Trigger>
											<DropdownMenu.Content class="w-56">
												<DropdownMenu.Group>
													<DropdownMenu.Item
														on:click={() => {
															renamePopoverOpen = true;
															renamingItem = i;
														}}
													>
														Rename
														<DropdownMenu.Shortcut>r</DropdownMenu.Shortcut>
													</DropdownMenu.Item>
												</DropdownMenu.Group>
												<DropdownMenu.Separator />
												<DropdownMenu.Group>
													<DropdownMenu.Item>
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
</main>
