import type { Tables } from './supabase';

export type UUID = `${string}-${string}-4${string}-${'89ab'}${string}-${string}`;

export type LeadData = {
	type: 'SUBMISSION' | 'COMMENT';
	url: string;
	title?: string;
	body?: string;
};

export type Lead = Tables<'leads'>;
