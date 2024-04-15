import createClient from 'openapi-fetch';
import type { paths, components } from '$lib/api/v0.d.ts';

const client = createClient<paths>({ baseUrl: 'https://api.aiti.no/' });
export default client;

type schemas = components['schemas'];
type headers = components['headers'];
type responses = components['responses'];
type parameters = components['parameters'];
type requestBodies = components['requestBodies'];
type pathItems = components['pathItems'];
export type { paths, schemas, headers, responses, parameters, requestBodies, pathItems };
