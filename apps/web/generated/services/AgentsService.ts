/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AgentRequestModel } from '../models/AgentRequestModel';
import type { AgentResponseModel } from '../models/AgentResponseModel';
import type { AgentUpdateModel } from '../models/AgentUpdateModel';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AgentsService {
    /**
     * Get Published Agents
     * @returns AgentResponseModel Successful Response
     * @throws ApiError
     */
    public static getPublishedAgentsAgentsPublishedGet(): CancelablePromise<Array<AgentResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/agents/published',
        });
    }
    /**
     * Get Users Agents
     * @param profileId
     * @returns AgentResponseModel Successful Response
     * @throws ApiError
     */
    public static getUsersAgentsAgentsByProfileGet(
        profileId: string,
    ): CancelablePromise<Array<AgentResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/agents/by_profile',
            query: {
                'profile_id': profileId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Agents From Crew
     * @param crewId
     * @returns AgentResponseModel Successful Response
     * @throws ApiError
     */
    public static getAgentsFromCrewAgentsByCrewGet(
        crewId: string,
    ): CancelablePromise<Array<AgentResponseModel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/agents/by_crew',
            query: {
                'crew_id': crewId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Agent By Id
     * @param agentId
     * @returns AgentResponseModel Successful Response
     * @throws ApiError
     */
    public static getAgentByIdAgentsAgentIdGet(
        agentId: string,
    ): CancelablePromise<AgentResponseModel> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/agents/{agent_id}',
            path: {
                'agent_id': agentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Patch Agent
     * @param agentId
     * @param requestBody
     * @returns AgentResponseModel Successful Response
     * @throws ApiError
     */
    public static patchAgentAgentsAgentIdPatch(
        agentId: string,
        requestBody: AgentUpdateModel,
    ): CancelablePromise<AgentResponseModel> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/agents/{agent_id}',
            path: {
                'agent_id': agentId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Agent
     * @param agentId
     * @returns AgentResponseModel Successful Response
     * @throws ApiError
     */
    public static deleteAgentAgentsAgentIdDelete(
        agentId: string,
    ): CancelablePromise<AgentResponseModel> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/agents/{agent_id}',
            path: {
                'agent_id': agentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Insert Agent
     * @param requestBody
     * @returns AgentResponseModel Successful Response
     * @throws ApiError
     */
    public static insertAgentAgentsPost(
        requestBody: AgentRequestModel,
    ): CancelablePromise<AgentResponseModel> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/agents/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
