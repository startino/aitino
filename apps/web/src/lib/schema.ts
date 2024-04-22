import { z } from 'zod';

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
	tools: z.array(z.record(z.string(), z.never())),
	system_message: z.string().min(20),
	model: z.union([z.literal('gpt-4-turbo'), z.literal('gpt-3.5-turbo')])
});
export type AgentSchema = typeof agentSchema;

// TODO: rename to createUserSchema
export const formSchema = z.object({
	display_name: z
		.string()
		.min(1, { message: 'Display Name is required' })
		.max(100, { message: 'Display Name must be 100 characters or less' }),
	email: z.string().email({ message: 'Invalid email address' }),
	password: z
		.string()
		.min(8, { message: 'Password must be at least 8 characters long.' })
		.max(100, { message: 'Password must be 100 characters or less.' })
		.regex(/[a-z]/, { message: 'Password must contain at least one lowercase letter.' })
		.regex(/[A-Z]/, { message: 'Password must contain at least one uppercase letter.' })
		.regex(/[0-9]/, { message: 'Password must contain at least one number.' })
});
export type FormSchema = typeof formSchema; // TODO: rename to CreateUserSchema

export const loginUserSchema = z.object({
	email: z.string().email({ message: 'Invalid email address' }),
	password: z
		.string()
		.min(8, { message: 'Password must be at least 8 characters long.' })
		.max(100, { message: 'Password must be 100 characters or less.' })
		.regex(/[a-z]/, { message: 'Password must contain at least one lowercase letter.' })
		.regex(/[A-Z]/, { message: 'Password must contain at least one uppercase letter.' })
		.regex(/[0-9]/, { message: 'Password must contain at least one number.' })
});
export type LoginUserSchema = typeof loginUserSchema;

export const waitlistSchema = z.object({
	email: z.string().email({ message: 'Invalid email address' })
});
export type WaitlistSchema = typeof waitlistSchema;
