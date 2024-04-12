import createClient from 'openapi-fetch';
import type { paths } from '$lib/api/v0.d.ts';

const client = createClient<paths>({ baseUrl: 'https://api.aiti.no/' });

export default client;
