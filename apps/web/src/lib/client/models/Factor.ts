/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * A MFA factor.
 */
export type Factor = {
    id: string;
    friendly_name?: (string | null);
    factor_type: string;
    status: Factor.status;
    created_at: string;
    updated_at: string;
};
export namespace Factor {
    export enum status {
        VERIFIED = 'verified',
        UNVERIFIED = 'unverified',
    }
}

