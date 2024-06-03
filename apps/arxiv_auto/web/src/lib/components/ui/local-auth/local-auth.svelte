<script lang="ts">
	import sha256 from 'crypto-js/sha256';
	import { Button } from '$lib/components/ui/button';

	// Double SHA256 hashed
	const key = 'f2d37b3fe684500fd54093e33446b49085626a7874b708d8c6dd9102499a493c';

	// Debug value, should login instance be remembered?
	const rememberKey = true;

	function reload() {
		window.location.reload();
	}

	function verify() {
		// Remove key from localStorage the key for debug purposes.
		if (!rememberKey) localStorage.setItem('key', '');

		// Check if the saved key in localStorage is correct, if so verify immediately.
		if (sha256(localStorage.getItem('key')) == key) return true;

		// First hashing with SHA256 so the original password cannot be read in localStorage
		// A second hashing of the input is performed only on checks to prevent copy pasting
		// the true key.
		localStorage.setItem('key', sha256(prompt('Enter Key', '')?.replace(/\s+/g, '')));

		// Log given hashes of input key.
		console.debug(
			`SHA256: ${localStorage.getItem('key')}\nDouble SHA256: ${sha256(
				localStorage.getItem('key')
			)}`
		);

		// Perform second hashing only when checking to prevent user from edeting their
		// localStorage to ensure they didn't copy paste the true key.
		return sha256(localStorage.getItem('key')) == key;
	}

	let verified: Promise<boolean> = new Promise((resolve, reject) => {
		try {
			resolve(verify());
		} catch {
			reject('Error with verification.');
		}
	});
</script>

{#await verified}
	<main class="grid h-screen grid-rows-3">
		<div class="row-start-2 grid place-items-center space-y-12">
			<h1 class="text-6xl">Authenticating...</h1>
		</div>
	</main>
{:then isVerified}
	{#if isVerified}
		<slot />
	{:else}
		<main class="grid h-screen grid-rows-3">
			<div class="row-start-2 grid place-items-center space-y-12">
				<h1 class="text-6xl">Failed authentication</h1>
				<h2 class="text-2xl">Please Refresh Page and enter the right key</h2>
				<button on:click={reload}>
					<Button>Refresh Page</Button>
				</button>
			</div>
		</main>
	{/if}
{/await}
