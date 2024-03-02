import { z } from "zod";

export const formSchema = z.object({
	display_name: z
		.string()
		.min(1, { message: "Display Name is required" })
		.max(100, { message: "Display Name must be 100 characters or less" }),
	email: z.string().email({ message: "Invalid email address" }),
	password: z
		.string()
		.min(8, { message: "Password must be at least 8 characters long." })
		.max(100, { message: "Password must be 100 characters or less." })
		.regex(/[a-z]/, { message: "Password must contain at least one lowercase letter." })
		.regex(/[A-Z]/, { message: "Password must contain at least one uppercase letter." })
		.regex(/[0-9]/, { message: "Password must contain at least one number." })
});

export type FormSchema = typeof formSchema;
