/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { APIKeyTypeResponseModel } from '../models/APIKeyTypeResponseModel';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ApiKeyTypesService {
    /**
     * Get All Api Key Types
     * @returns APIKeyTypeResponseModel Successful Response
     * @throws ApiError
     */
    public static getAllApiKeyTypesApiKeyTypesGet(): CancelablePromise<Array<APIKeyTypeResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api_key_types/',
        });
    }
}
