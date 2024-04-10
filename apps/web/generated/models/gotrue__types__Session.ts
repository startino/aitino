/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { User } from './User';
export type gotrue__types__Session = {
    provider_token?: (string | null);
    provider_refresh_token?: (string | null);
    access_token: string;
    refresh_token: string;
    expires_in: number;
    expires_at?: (number | null);
    token_type: string;
    user: User;
};

