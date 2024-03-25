<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import type { NoSessionLoad } from '$lib/types/loads';
	import { PUBLIC_API_URL } from '$env/static/public';
	import * as models from '$lib/types/models';

	export let data: NoSessionLoad;

    let profileId: string = data.profileId;
	let crews: models.Crew[] = data.crews;

	async function startNewSession(crew: models.Crew, title: string) {
		// Instantiate and get the new session
		const res = await fetch(`${PUBLIC_API_URL}/crew?id=${crew.id}&profile_id=${profileId}`)
			.then((response) => {
				if (response.status === 200) {
					return response.json();
				} else {
					throw new Error('Failed to start new session. bad respose: ' + response);
				}
			})
			.catch((error) => {
				console.error('Failed to start new session. error', error);
			});

		const session: models.Session = res.data.session;

		window.location.href = '/app/session/' + session.id;  // Can this be done better without full page reload?
	}
</script>

{#if crews}
	<div
		class="xl:prose-md prose prose-sm prose-main mx-auto flex h-screen max-w-none flex-col items-center justify-center gap-4 px-12 text-center md:prose-base 2xl:prose-lg"
	>
		<h1>It looks like you haven't started a session yet...</h1>
		{#if crews}
			<!-- Allow user to choose crew -->
			<Button on:click={() => startNewSession(crews[0], 'New Session')}>Run Your Crew!</Button>
		{:else}
			<p>Loading...</p>
		{/if}
	</div>
{:else}
	<div
		class="xl:prose-md prose prose-sm prose-main mx-auto mt-auto flex h-full max-w-none flex-col items-center justify-center gap-4 px-12 text-center md:prose-base 2xl:prose-lg"
	>
		<h1>Looks like you haven't created your own crew yet...</h1>
	</div>
{/if}
