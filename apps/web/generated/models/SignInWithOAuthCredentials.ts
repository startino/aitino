/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SignInWithOAuthCredentialsOptions } from './SignInWithOAuthCredentialsOptions';
export type SignInWithOAuthCredentials = {
    provider: SignInWithOAuthCredentials.provider;
    options?: SignInWithOAuthCredentialsOptions;
};
export namespace SignInWithOAuthCredentials {
    export enum provider {
        APPLE = 'apple',
        AZURE = 'azure',
        BITBUCKET = 'bitbucket',
        DISCORD = 'discord',
        FACEBOOK = 'facebook',
        FIGMA = 'figma',
        GITHUB = 'github',
        GITLAB = 'gitlab',
        GOOGLE = 'google',
        KAKAO = 'kakao',
        KEYCLOAK = 'keycloak',
        LINKEDIN = 'linkedin',
        NOTION = 'notion',
        SLACK = 'slack',
        SPOTIFY = 'spotify',
        TWITCH = 'twitch',
        TWITTER = 'twitter',
        WORKOS = 'workos',
        ZOOM = 'zoom',
    }
}

