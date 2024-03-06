// @ts-nocheck
import type { LayoutServerLoad } from "./$types";

// src/routes/+layout.server.ts
export const load = async ({ locals: { getSession } }: Parameters<LayoutServerLoad>[0]) => {
	return {
		session: await getSession()
	};
};
