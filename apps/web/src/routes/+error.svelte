<script>
	import { page } from '$app/stores';

	const { status, error } = $page;
</script>

<svelte:head>
	<title>{status} {error}</title>
</svelte:head>

<main class="grid h-screen min-h-full place-items-center px-6 py-24 sm:py-32 lg:px-8">
	<div class="text-center">
		<p class="text-base font-semibold text-primary">{status}</p>
		<h1 class="mt-4 text-3xl font-bold tracking-tight text-foreground sm:text-5xl">
			{error?.message}
		</h1>
		<p class="mt-6 text-base leading-7 text-foreground/70">
			{status == 404 ? 'Sorry, we couldn’t find the page you’re looking for.' : ''}
		</p>
		<div class="mt-10 flex items-center justify-center gap-x-6">
			<a
				href="/"
				class="rounded-md bg-primary px-3.5 py-2.5 text-sm font-semibold text-primary-foreground shadow-sm hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
			>
				Go back home
			</a>
			<a href="/blog" class="text-sm font-semibold text-foreground/70">
				Check out the blog <span aria-hidden="true">&rarr;</span>
			</a>
		</div>
	</div>
</main>
