import { z } from 'zod';

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

export const waitlistSchema = z.object({
	email: z.string().email({ message: 'Invalid email address' })
});

export const createNewAgents = z.object({
	id: z.string(),
	title: z
		.string()
		.min(1, { message: 'Title must not be empty' })
		.max(100, { message: 'Title must be 100 characters or less' }),
	role: z
		.string()
		.min(1, { message: 'Role must not be empty' })
		.max(100, { message: 'Role must be 100 characters or less' }),
	description: z
		.string()
		.min(10, { message: 'Description must be at least 20 characters' })
		.max(1000, { message: 'Description must be 1000 characters or less' }),
	published: z.string(),
	tools: z.string(),
	system_message: z.string(),
	model: z.string()
});

export type FormSchema = typeof formSchema;
export type AgentFormSchema = typeof createNewAgents;
