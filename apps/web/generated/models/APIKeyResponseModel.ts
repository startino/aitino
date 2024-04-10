/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { APIKeyTypeModel } from './APIKeyTypeModel';
export type APIKeyResponseModel = {
    id: string;
    created_at: string;
    profile_id: string;
    api_key_type?: (APIKeyTypeModel | null);
    api_key: string;
};

