import { z } from 'zod';

export const contactSchema = z.object({
	name: z.string().trim().min(1).max(30),
	email: z.string().trim().email({ message: 'Invalid email address' }),
	description: z.string().trim().min(20).max(500)
});
export type ContactSchema = typeof contactSchema;

export const waitlistSchema = z.object({
	email: z.string().trim().email({ message: 'Invalid email address' })
});
export type WaitlistSchema = typeof waitlistSchema;

export const promptSchema = z.object({
	email: z.string().trim().email({ message: 'Invalid email address' })
});
export type PromptSchema = typeof promptSchema;

export const apiKeySchema = z.object({
	typeId: z.string().min(1, 'An API Key Type is required'),
	value: z.string().min(1, 'The value of the key is required')
});
export type ApiKeySchema = typeof apiKeySchema;

export const editCrewSchema = z.object({
	id: z.string(),
	title: z.string().default('Untitled'),
	description: z.string().default('No description'),
	published: z.boolean().default(false)
});
export type EditCrewSchema = typeof editCrewSchema;

export const createCrewSchema = z.object({
	title: z.string().min(1).max(50),
	description: z.string().max(500).default(''),
	published: z.boolean().default(false)
});
export type CreateCrewSchema = typeof createCrewSchema;

export const agentSchema = z.object({
	id: z.string(),
	title: z.string().min(1).max(50),
	description: z.string().max(500).default(''),
	published: z.boolean().default(false),
	role: z.string().min(1).max(50),
	tools: z.array(z.any()),
	system_message: z.string().min(20),
	model: z.union([z.literal('gpt-4-turbo'), z.literal('gpt-35-turbo')], z.literal('gpt-4'))
});
export type AgentSchema = typeof agentSchema;

export const emailAuthSchema = z.object({
	email: z.string().email({ message: 'Invalid email address' })
});
export type EmailAuthSchema = typeof emailAuthSchema; // TODO: rename to CreateUserSchema
