// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces

import { SupabaseClient, User, Session } from '@supabase/supabase-js';
import type Stripe from 'stripe';

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			supabase: SupabaseClient;
			stripe: Stripe;
			safeGetSession(): Promise<{ session: Session; user: User } | null>;
			authGetSession(): Promise<{ session: Session; user: User }>;
		}
		interface PageData {
			session: Session | null;
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
