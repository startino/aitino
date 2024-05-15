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
			getUser(): Promise<(User & schemas['Profile']) | null>;
			authGetUser(): Promise<User & schemas['Profile']>;
			safeGetSession(): Promise<(Session & User & schemas['Profile']) | null>;
			authGetSession(): Promise<Session & User & schemas['Profile']>;
		}
		interface PageData {
			session: Session | null;
		}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
