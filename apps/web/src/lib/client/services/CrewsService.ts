/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CrewRequestModel } from '../models/CrewRequestModel';
import type { CrewResponseModel } from '../models/CrewResponseModel';
import type { CrewUpdateModel } from '../models/CrewUpdateModel';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CrewsService {
    /**
     * Insert Crew
     * @param requestBody
     * @returns CrewResponseModel Successful Response
     * @throws ApiError
     */
    public static insertCrewCrewsPost(
        requestBody: CrewRequestModel,
    ): CancelablePromise<CrewResponseModel> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/crews/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get User Crews
     * @param profileId
     * @param ascending
     * @returns CrewResponseModel Successful Response
     * @throws ApiError
     */
    public static getUserCrewsCrewsProfileIdGet(
        profileId: string,
        ascending: boolean = true,
    ): CancelablePromise<Array<CrewResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/crews/{profile_id}',
            path: {
                'profile_id': profileId,
            },
            query: {
                'ascending': ascending,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Crew
     * @param crewId
     * @returns CrewResponseModel Successful Response
     * @throws ApiError
     */
    public static getCrewCrewsCrewIdGet(
        crewId: string,
    ): CancelablePromise<CrewResponseModel> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/crews/{crew_id}',
            path: {
                'crew_id': crewId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Crew
     * @param crewId
     * @param requestBody
     * @returns CrewResponseModel Successful Response
     * @throws ApiError
     */
    public static updateCrewCrewsCrewIdPatch(
        crewId: string,
        requestBody: CrewUpdateModel,
    ): CancelablePromise<CrewResponseModel> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/crews/{crew_id}',
            path: {
                'crew_id': crewId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Published Crews
     * @returns CrewResponseModel Successful Response
     * @throws ApiError
     */
    public static getPublishedCrewsCrewsPublishedGet(): CancelablePromise<Array<CrewResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/crews/published',
        });
    }
}
