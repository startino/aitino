import { z } from 'zod';

export const formSchema = z.object({
	name: z.string().trim().min(1).max(30),
	email: z.string().trim().email({ message: 'Invalid email address' }),
	description: z.string().trim().min(20).max(500)
});

export const waitlistSchema = z.object({
	email: z.string().trim().email({ message: 'Invalid email address' })
});

export const promptSchema = z.object({
	email: z.string().trim().email({ message: 'Invalid email address' })
});

export type FormSchema = typeof formSchema;
export type WaitlistSchema = typeof waitlistSchema;
export type promptSchema = typeof promptSchema;
