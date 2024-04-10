/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type AgentModel = {
    title: string;
    role: string;
    system_message: string;
    tools: Array<Record<string, any>>;
    model: AgentModel.model;
    id: string;
};
export namespace AgentModel {
    export enum model {
        GPT_3_5_TURBO = 'gpt-3.5-turbo',
        GPT_4_TURBO_PREVIEW = 'gpt-4-turbo-preview',
    }
}

