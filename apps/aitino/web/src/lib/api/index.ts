import createClient from 'openapi-fetch';
import type { paths, components } from '$lib/api/v0.d.ts';
import { PUBLIC_API_URI } from '$env/static/public';

const api = createClient<paths>({ baseUrl: PUBLIC_API_URI });
export default api;

type schemas = components['schemas'];
type headers = components['headers'];
type responses = components['responses'];
type parameters = components['parameters'];
type requestBodies = components['requestBodies'];
type pathItems = components['pathItems'];
export type { paths, schemas, headers, responses, parameters, requestBodies, pathItems };
