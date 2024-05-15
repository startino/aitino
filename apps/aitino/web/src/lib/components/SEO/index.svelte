<script lang="ts">
	import website from '$lib/config/website';
	import OpenGraph from './OpenGraph.svelte';
	import Twitter from './Twitter.svelte';
	import type { SEOImage } from './types';

	let favIconSrc = '/favicon.png';

	const {
		author,
		facebookAuthorPage,
		facebookPage,
		ogLanguage,
		siteLanguage,
		siteShortTitle,
		siteTitle,
		siteUrl,
		githubPage,
		linkedinProfile,
		telegramUsername,
		tiktokUsername,
		twitterUsername
	} = website;

	export let article = false;
	export let lastUpdated = '';
	export let datePublished = '';
	export let metadescription: string;
	export let slug;
	export let timeToRead = 0;
	export let title;

	const defaultAlt = 'a picture of an ai agent';

	export let ogImage: SEOImage | null = {
		url: favIconSrc,
		alt: defaultAlt
	};
	export let ogSquareImage: SEOImage | null = {
		url: favIconSrc,
		alt: defaultAlt
	};
	export let twitterImage: SEOImage | null = {
		url: favIconSrc,
		alt: defaultAlt
	};
	const url = `${siteUrl}/${slug}`;
	const pageTitle = `${siteTitle} | ${title}`;
	const openGraphProps = {
		article,
		datePublished,
		lastUpdated,
		image: ogImage,
		squareImage: ogSquareImage,
		metadescription,
		ogLanguage,
		pageTitle,
		siteTitle,
		url,
		...(article ? { datePublished, lastUpdated, facebookPage, facebookAuthorPage } : {})
	};

	const twitterProps = {
		article,
		author,
		twitterUsername,
		image: twitterImage,
		timeToRead
	};
</script>

<svelte:head>
	<title>{pageTitle}</title>
	<meta name="description" content={metadescription} />
	<meta
		name="robots"
		content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"
	/>
</svelte:head>
<Twitter {...twitterProps} />
<OpenGraph {...openGraphProps} />
