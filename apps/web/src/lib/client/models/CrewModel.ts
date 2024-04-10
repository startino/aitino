/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AgentModel } from './AgentModel';
export type CrewModel = {
    receiver_id: string;
    delegator_id?: (string | null);
    agents: Array<AgentModel>;
    sub_crews?: Array<CrewModel>;
};

