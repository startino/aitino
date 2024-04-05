/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CrewResponseModel = {
    id: string;
    created_at: string;
    profile_id: string;
    edges: Array<Record<string, any>>;
    published: boolean;
    title: string;
    description: string;
    updated_at: string;
    nodes: Array<string>;
    receiver_id?: (string | null);
    avatar?: (string | null);
    prompt?: (Record<string, any> | null);
};

