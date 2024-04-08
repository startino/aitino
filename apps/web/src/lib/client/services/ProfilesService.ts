/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { APIKeyRequestModel } from '../models/APIKeyRequestModel';
import type { APIKeyResponseModel } from '../models/APIKeyResponseModel';
import type { APIKeyUpdateModel } from '../models/APIKeyUpdateModel';
import type { ProfileRequestModel } from '../models/ProfileRequestModel';
import type { ProfileResponseModel } from '../models/ProfileResponseModel';
import type { ProfileUpdateModel } from '../models/ProfileUpdateModel';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ProfilesService {
    /**
     * Get Profiles
     * @returns ProfileResponseModel Successful Response
     * @throws ApiError
     */
    public static getProfilesProfilesGet(): CancelablePromise<Array<ProfileResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/profiles/',
        });
    }
    /**
     * Insert Profile
     * @param requestBody
     * @returns ProfileResponseModel Successful Response
     * @throws ApiError
     */
    public static insertProfileProfilesPost(
        requestBody: ProfileRequestModel,
    ): CancelablePromise<ProfileResponseModel> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/profiles/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Profile
     * @param profileId
     * @returns ProfileResponseModel Successful Response
     * @throws ApiError
     */
    public static getProfileProfilesProfileIdGet(
        profileId: string,
    ): CancelablePromise<ProfileResponseModel> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/profiles/{profile_id}',
            path: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Profile
     * @param profileId
     * @param requestBody
     * @returns ProfileResponseModel Successful Response
     * @throws ApiError
     */
    public static updateProfileProfilesProfileIdPatch(
        profileId: string,
        requestBody: ProfileUpdateModel,
    ): CancelablePromise<ProfileResponseModel> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/profiles/{profile_id}',
            path: {
                'profile_id': profileId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Api Keys
     * Returns api keys with the format: {api_key_type_id: api_key}.
     * @param profileId
     * @returns APIKeyResponseModel Successful Response
     * @throws ApiError
     */
    public static getApiKeysProfilesProfileIdApiKeysGet(
        profileId: string,
    ): CancelablePromise<Array<APIKeyResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/profiles/{profile_id}/api_keys',
            path: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Insert Api Key
     * @param requestBody
     * @returns APIKeyResponseModel Successful Response
     * @throws ApiError
     */
    public static insertApiKeyProfilesApiKeysPost(
        requestBody: APIKeyRequestModel,
    ): CancelablePromise<APIKeyResponseModel> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/profiles/api_keys',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Api Key
     * @param apiKeyId
     * @returns APIKeyResponseModel Successful Response
     * @throws ApiError
     */
    public static deleteApiKeyProfilesApiKeysApiKeyIdDelete(
        apiKeyId: string,
    ): CancelablePromise<APIKeyResponseModel> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/profiles/api_keys/{api_key_id}',
            path: {
                'api_key_id': apiKeyId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Api Key
     * @param apiKeyId
     * @param requestBody
     * @returns APIKeyResponseModel Successful Response
     * @throws ApiError
     */
    public static updateApiKeyProfilesApiKeysApiKeyIdPatch(
        apiKeyId: string,
        requestBody: APIKeyUpdateModel,
    ): CancelablePromise<APIKeyResponseModel> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/profiles/api_keys/{api_key_id}',
            path: {
                'api_key_id': apiKeyId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
