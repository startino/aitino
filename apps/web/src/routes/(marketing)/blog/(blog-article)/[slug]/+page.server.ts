import type { SvelteComponent } from 'svelte';
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import { base } from '$app/paths';
import { get_blog_data, get_processed_blog_post } from '$lib/server/blog/index.js';
import type { BlogPost } from '$lib/server/blog/types';

const prerender = 'auto';

export const load: PageServerLoad = async ({ params }) => {
	const post: BlogPost | null = await get_processed_blog_post(await get_blog_data(), params.slug);

	if (!post) {
		throw error(404, "Could not find the blog post you're looking for.");
	}

	return {
		post
	};
};
