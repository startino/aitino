/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Factor } from './Factor';
import type { UserIdentity } from './UserIdentity';
export type User = {
    id: string;
    app_metadata: Record<string, any>;
    user_metadata: Record<string, any>;
    aud: string;
    confirmation_sent_at?: (string | null);
    recovery_sent_at?: (string | null);
    email_change_sent_at?: (string | null);
    new_email?: (string | null);
    invited_at?: (string | null);
    action_link?: (string | null);
    email?: (string | null);
    phone?: (string | null);
    created_at: string;
    confirmed_at?: (string | null);
    email_confirmed_at?: (string | null);
    phone_confirmed_at?: (string | null);
    last_sign_in_at?: (string | null);
    role?: (string | null);
    updated_at?: (string | null);
    identities?: (Array<UserIdentity> | null);
    factors?: (Array<Factor> | null);
};

