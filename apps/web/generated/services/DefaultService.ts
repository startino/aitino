/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CrewModel } from '../models/CrewModel';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DefaultService {
    /**
     * Redirect To Docs
     * @returns any Successful Response
     * @throws ApiError
     */
    public static redirectToDocsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }
    /**
     * Compile
     * @param id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static compileCompileGet(
        id: string,
    ): CancelablePromise<Record<string, (string | CrewModel)>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/compile',
            query: {
                'id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Improve
     * @param wordLimit
     * @param prompt
     * @param promptType
     * @param temperature
     * @param profileId
     * @returns string Successful Response
     * @throws ApiError
     */
    public static improveImproveGet(
        wordLimit: number,
        prompt: string,
        promptType: 'generic' | 'system' | 'user',
        temperature: number,
        profileId: string,
    ): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/improve',
            query: {
                'word_limit': wordLimit,
                'prompt': prompt,
                'prompt_type': promptType,
                'temperature': temperature,
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Auto Build Crew
     * @param generalTask
     * @param profileId
     * @returns string Successful Response
     * @throws ApiError
     */
    public static autoBuildCrewAutoBuildGet(
        generalTask: string,
        profileId: string,
    ): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auto-build',
            query: {
                'general_task': generalTask,
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Profile From Header
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getProfileFromHeaderMeGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/me',
        });
    }
}
