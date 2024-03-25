import { Carta } from 'carta-md';
import type { BlogData, BlogPost, MarkdownMetadata } from './types';
import type { SvelteComponent } from 'svelte';
import { error } from '@sveltejs/kit';
import { base } from '$app/paths';

const BLOG_PATH = `./src/lib/documentation/blog`;

export async function get_blog_post(pathname: string) {
	const pages = import.meta.glob('./src/lib/documentation/blog/*.md');
	const path = pathname.slice(base.length).slice(1).split('/').pop();
	const match = pages[`./src/lib/documentation/blog/${path}.md`];
	if (!match) throw error(404, "Could not find the blog post you're looking for.");

	const Markdown = (await match()) as {
		default: SvelteComponent;
		metadata: MarkdownMetadata;
	};
	return Markdown;
}

export async function get_processed_blog_post(
	blog_data: BlogData,
	slug: string
): Promise<BlogPost | null> {
	const carta = new Carta({});
	for (const post of blog_data) {
		if (post.metadata.slug === slug) {
			return {
				...post,
				content: await carta.render(post.content)
			};
		}
	}

	return null;
}

const BLOG_NAME_REGEX = /^(\d{4}-\d{2}-\d{2})-(.+)\.md$/;

export async function get_blog_data(base = BLOG_PATH): Promise<BlogData> {
	const { readdir, readFile } = await import('node:fs/promises');

	const blog_posts: BlogData = [];

	for (const file of (await readdir(base)).reverse()) {
		if (!BLOG_NAME_REGEX.test(file)) continue;

		const { date, date_formatted, slug } = get_date_and_slug(file);
		const { metadata, body } = extractFrontmatter(await readFile(`${base}/${file}`, 'utf-8'));

		blog_posts.push({
			metadata: {
				date,
				date_formatted,
				description: metadata?.description ?? '',
				published: metadata?.published ?? false,
				slug,
				title: metadata?.title ?? '',
				file,
				author: metadata?.author ?? 'Aitino',
				thumbnail: metadata?.thumbnail ?? 'favicon.png'
			},
			content: body
		});
	}

	return blog_posts;
}

export function get_blog_list(blog_data: BlogData) {
	console.log('blog_data', blog_data);
	return blog_data.map(
		({
			metadata: {
				slug,
				date,
				title,
				description,
				published,
				thumbnail,
				date_formatted,
				author,
				category
			}
		}) => ({
			slug,
			date,
			title,
			description,
			published,
			thumbnail,
			date_formatted,
			author,
			category
		})
	);
}

export function get_date_and_slug(filename: string) {
	const match = BLOG_NAME_REGEX.exec(filename);
	if (!match) throw new Error(`Invalid filename for blog: '${filename}'`);

	const [, date, slug] = match;
	const [y, m, d] = date.split('-');
	const date_formatted = `${months[+m - 1]} ${+d}, ${y}`;

	return { date, date_formatted, slug };
}

const months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ');

// Markdown
export function extractFrontmatter(markdown: string) {
	const match = /---\r?\n([\s\S]+?)\r?\n---/.exec(markdown);
	if (!match) return { metadata: null, body: markdown };

	const frontmatter = match[1];
	const body = markdown.slice(match[0].length);

	let metadata: MarkdownMetadata = {} as MarkdownMetadata;

	frontmatter.split('\n').forEach((pair) => {
		const items = pair.split(':');
		const [key, value] = [items[0], items.slice(1).join(':')];
		if (key && value) {
			metadata[key] = removeQuotes(value).trim();
		}
	});

	return { metadata, body };
}

export function removeQuotes(text: string) {
	return text.replace(/"/g, '');
}
