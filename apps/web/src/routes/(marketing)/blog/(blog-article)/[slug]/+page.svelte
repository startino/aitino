<script lang="ts">
	import { onMount, type SvelteComponent } from 'svelte';
	import SEO from '$lib/components/SEO/index.svelte';
	import { page } from '$app/stores';

	import { base } from '$app/paths';

	export let data;

	const {
		post: { metadata, content }
	} = data;
</script>

<SEO
	article
	slug={metadata.slug}
	title={metadata.title}
	datePublished={metadata.date}
	metadescription={metadata.description}
	lastUpdated={metadata.date}
/>

<article
	class="sm:prose-md prose prose-blog mx-auto max-w-none px-4 md:prose-lg xl:prose-xl"
	data-pubdate={metadata.date}
>
	<div
		class="mx-auto mb-20 flex max-w-prose flex-col items-start md:mb-32 lg:mb-36 lg:max-w-6xl lg:place-items-center"
	>
		<h1 class="mb-2 text-balance font-semibold text-foreground sm:mb-4 lg:text-center">
			{metadata.title}
		</h1>
		<div class="flex flex-row place-items-center gap-x-6 text-sm">
			<div class="relative flex items-center gap-x-4">
				<img
					src={metadata.author == 'Jorge Lewis'
						? '/people/jorge-lewis.png'
						: metadata.author == 'Jonas Lindberg'
							? '/people/jonas-lindberg.jpg'
							: '/favicon.png'}
					alt="{metadata.author}'s Profile Picture"
					class="not-prose h-10 w-10 rounded-full bg-card"
				/>
				<div class="leading-6">
					<p class="font-semibold text-foreground">By {metadata.author}</p>
				</div>
			</div>
			<time datetime={metadata.date} class="font-semibold text-foreground/70"
				>{metadata.date_formatted}</time
			>
		</div>
		<div class="relative aspect-1 w-full max-w-prose shrink-0">
			<img
				src={metadata.thumbnail}
				alt="Thumbnail for {metadata.title}"
				class="absolute inset-0 h-full w-full rounded-2xl bg-card object-cover"
			/>
			<div class="absolute inset-0 rounded-2xl ring-1 ring-inset ring-background/10"></div>
		</div>
	</div>

	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	<div class="mx-auto max-w-prose">
		{@html content}
	</div>
</article>
