/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Message } from '../models/Message';
import type { RunRequestModel } from '../models/RunRequestModel';
import type { RunResponseModel } from '../models/RunResponseModel';
import type { SessionRequest } from '../models/SessionRequest';
import type { SessionResponse } from '../models/SessionResponse';
import type { SessionUpdate } from '../models/SessionUpdate';
import type { src__models__session__Session } from '../models/src__models__session__Session';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SessionsService {
    /**
     * Get Sessions
     * @param profileId
     * @param sessionId
     * @returns src__models__session__Session Successful Response
     * @throws ApiError
     */
    public static getSessionsSessionsGet(
        profileId?: (string | null),
        sessionId?: (string | null),
    ): CancelablePromise<Array<src__models__session__Session>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sessions/',
            query: {
                'profile_id': profileId,
                'session_id': sessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Insert Session
     * @param requestBody
     * @returns SessionResponse Successful Response
     * @throws ApiError
     */
    public static insertSessionSessionsPost(
        requestBody: SessionRequest,
    ): CancelablePromise<SessionResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sessions/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Session
     * @param sessionId
     * @param requestBody
     * @returns SessionResponse Successful Response
     * @throws ApiError
     */
    public static updateSessionSessionsSessionIdPatch(
        sessionId: string,
        requestBody: SessionUpdate,
    ): CancelablePromise<SessionResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/sessions/{session_id}',
            path: {
                'session_id': sessionId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Session
     * @param sessionId
     * @returns void
     * @throws ApiError
     */
    public static deleteSessionSessionsSessionIdDelete(
        sessionId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/sessions/{session_id}',
            path: {
                'session_id': sessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Run Crew
     * @param requestBody
     * @param mock
     * @returns RunResponseModel Successful Response
     * @throws ApiError
     */
    public static runCrewSessionsRunPost(
        requestBody: RunRequestModel,
        mock: boolean = false,
    ): CancelablePromise<RunResponseModel> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sessions/run',
            query: {
                'mock': mock,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Messages
     * @param sessionId
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static getMessagesSessionsMessagesGet(
        sessionId: string,
    ): CancelablePromise<Array<Message>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sessions/messages/',
            query: {
                'session_id': sessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
