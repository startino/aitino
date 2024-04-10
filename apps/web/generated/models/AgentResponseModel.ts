/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type AgentResponseModel = {
    title: string;
    role: string;
    system_message: string;
    tools: Array<Record<string, any>>;
    model: AgentResponseModel.model;
    description?: (string | null);
    profile_id: string;
    version?: (string | null);
    avatar: string;
    id: string;
    created_at: string;
    published: boolean;
};
export namespace AgentResponseModel {
    export enum model {
        GPT_3_5_TURBO = 'gpt-3.5-turbo',
        GPT_4_TURBO_PREVIEW = 'gpt-4-turbo-preview',
    }
}

