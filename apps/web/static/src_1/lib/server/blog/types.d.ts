export interface BlogPost {
	metadata: MarkdownMetadata;
	content: string;
}

export type BlogData = BlogPost[];

export interface BlogPostSummary {
	slug: string;
	title: string;
	description: string;
	date: string;
	date_formatted: string;
	published: boolean;
	thumbnail: string;
	author: string;
}

export type MarkdownMetadata = {
	title: string;
	description: string;
	date: string;
	date_formatted: string;
	slug: string;
	file: string;
	author: string;
	published: boolean;
	thumbnail: string;
};
