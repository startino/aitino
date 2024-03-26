<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as Sheet from '$lib/components/ui/sheet';
	import * as utils from '$lib/utils';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { ScrollArea } from '$lib/components/ui/scroll-area/index.js';
	import * as Dialog from '$lib/components/ui/dialog';
	import { ArrowLeftFromLine, CheckCircle, PencilLine, Trash2, Loader } from 'lucide-svelte';
	import type { Crew, Session } from '$lib/types/models';
	import { PUBLIC_API_URL } from '$env/static/public';
	import * as models from '$lib/types/models';
	import * as api from '$lib/api';
	import type { UUID } from '$lib/types';

	export let profileId: string;
	export let sessions: Session[];
	export let crew: Crew | null;
	export let session: Session | null;

	let newSessionName: string = '';

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

		// If no session is being renamed, ignore
		if (!session) {
			resetRenamingUI();
			return;
		}
		// If no changes were made or if empty, reset the UI and ignore
		if (session?.title == renamingValue && renamingValue === '') {
			resetRenamingUI();
			return;
		}

		renamingInProgress = true;
		console.log('renaming', renamingValue, sessionId);

		api.upsertSession(session.id as UUID, { title: renamingValue });

		// Update the session locally in order to not refetch
		sessions = sessions.map((session) => {
			if (session.id === sessionId) {
				session.title = renamingValue;
			}
			return session as Session;
		});

		// Reset the renaming variables
		resetRenamingUI();
	}

	async function deleteSession(sessionId: string) {
		console.log('Deleting session', sessionId);
		deletingInProgress = true;
		deletingSession = sessionId;

		const success: boolean = await api.deleteSession(sessionId as UUID);

		if (!success) {
			console.error('Failed to delete session');
			return;
		}
		console.log('Successfully deleted session');

		// Update the session locally in order to not refetch
		sessions = sessions.filter((session) => session.id !== sessionId);
		resetDeletingUI();

		if (session?.id === sessionId) {
			window.location.href = '/app/session/';
		}
	}

	async function loadSession(session: models.Session) {
		console.log('Loading session', JSON.stringify(session));
		window.location.href = '/app/session/' + session.id; // Can this be done better without full page reload?
	}

	async function startNewSession(profileId: string, crewId: string, title: string) {
		const session = await api.startSession(profileId as UUID, crewId as UUID, title);

		if (!session) {
			console.error('Failed to start session');
			return;
		}

		window.location.href = '/app/session/' + session.id; // Can this be done better without full page reload?
	}
</script>

<Sheet.Root>
	<Sheet.Trigger asChild let:builder>
		<Button builders={[builder]} class="my-auto mr-8 h-14 w-14">
			<ArrowLeftFromLine size="24" />
		</Button>
	</Sheet.Trigger>
	<Sheet.Content side="right">
		<Sheet.Header>
			<Sheet.Description>
				{#if session}
					Click anywhere on the left to continue with your most recent session
				{:else}
					Create a new session or select an existing one
				{/if}
			</Sheet.Description>
		</Sheet.Header>

		<Sheet.Footer class="mt-2">
			<Sheet.Close asChild let:builder>
				<div class="flex h-full w-full flex-col gap-2">
					{#if crew}
						<Dialog.Root>
							<Dialog.Trigger let:builder>
								<Button class="mb-2 w-full" builders={[builder]}>Start New Session</Button>
							</Dialog.Trigger>
							<Dialog.Content class="sm:max-w-[425px]">
								<Dialog.Header>
									<Dialog.Title>Create a new Session</Dialog.Title>
									<Dialog.Description>
										Run a multi-agent simulation with your crew. (Only your most recent crew is
										available until later versions.)
									</Dialog.Description>
								</Dialog.Header>
								<div class="grid gap-4 py-4">
									<div class="grid grid-cols-4 items-center gap-4">
										<Label for="name" class="text-right">Name</Label>
										<Input
											id="name"
											placeholder="Session Name Here"
											bind:value={newSessionName}
											class="col-span-3"
										/>
									</div>
									<div class="grid grid-cols-4 items-center gap-4">
										<Label for="username" class="text-right">Crew</Label>
										<Button disabled variant="outline" class="col-span-3 w-full text-left">
											{crew.title}
										</Button>
									</div>
								</div>
								<Dialog.Footer>
									<Button
										builders={[builder]}
										on:click={() => startNewSession(profileId, crew.id, newSessionName)}
										>Start Session</Button
									>
								</Dialog.Footer>
							</Dialog.Content>
						</Dialog.Root>
					{/if}
					<ScrollArea class="flex h-full max-h-[85vh] w-full flex-col rounded-md pr-4">
						{#if !sessions}
							<p>Loading...</p>
						{:else}
							{#each sessions as session}
								<li class="my-3 flex w-full flex-row gap-4">
									{#if renamePopoverOpen && renamingSession === session.id}
										<Input
											type="text"
											class="w-full px-0.5"
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
											class="p-2"
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
											variant="icon"
											class="p-2"
											on:click={() => {
												renamePopoverOpen = true;
												renamingSession = session.id;
											}}
										>
											<PencilLine size="18" />
										</Button>
										<Button
											builders={[builder]}
											variant="outline"
											class="flex w-full flex-row justify-between {session?.id == session.id
												? 'bg-accent text-accent-foreground'
												: 'hover:bg-accent/20 hover:text-foreground'}"
											on:click={() => loadSession(session)}
										>
											{session.title}
											<div class="	text-right text-xs">
												Last opened {utils.daysRelativeToToday(session.created_at).toLowerCase()}
											</div>
										</Button>
										<Button
											variant="icon"
											class="p-2"
											on:click={() => {
												deleteSession(session.id);
											}}
										>
											{#if deletingInProgress && deletingSession === session.id}
												<Loader size="18" class="mx-auto my-auto " />
											{:else}
												<Trash2 size="18" />
											{/if}
										</Button>
									{/if}
								</li>
							{/each}
						{/if}
					</ScrollArea>
				</div>
			</Sheet.Close>
		</Sheet.Footer>
	</Sheet.Content>
</Sheet.Root>
