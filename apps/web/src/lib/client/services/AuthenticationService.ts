/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AuthResponse } from '../models/AuthResponse';
import type { OAuthResponse } from '../models/OAuthResponse';
import type { SignInWithEmailAndPasswordCredentials } from '../models/SignInWithEmailAndPasswordCredentials';
import type { SignInWithOAuthCredentials } from '../models/SignInWithOAuthCredentials';
import type { SignUpWithEmailAndPasswordCredentials } from '../models/SignUpWithEmailAndPasswordCredentials';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthenticationService {
    /**
     * Email Sign Up
     * format for passing display name: 'options': {'data':{'display_name': 'name'}}
     * @param requestBody
     * @returns AuthResponse Successful Response
     * @throws ApiError
     */
    public static emailSignUpAuthSignUpPost(
        requestBody: SignUpWithEmailAndPasswordCredentials,
    ): CancelablePromise<AuthResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/sign_up',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Email Sign In
     * @param requestBody
     * @returns AuthResponse Successful Response
     * @throws ApiError
     */
    public static emailSignInAuthSignInPost(
        requestBody: SignInWithEmailAndPasswordCredentials,
    ): CancelablePromise<AuthResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/sign_in',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Provider Sign In
     * @param requestBody
     * @returns OAuthResponse Successful Response
     * @throws ApiError
     */
    public static providerSignInAuthSignInProviderPost(
        requestBody: SignInWithOAuthCredentials,
    ): CancelablePromise<OAuthResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/sign_in/provider',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
