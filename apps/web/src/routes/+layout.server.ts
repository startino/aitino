import api from '$lib/api';
import { crewSchema, agentSchema } from '$lib/schema';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';

export const load = async ({ url, locals: { getUser, supabase } }) => {
	const code = url.searchParams.get('code');
	const user = await getUser();

	if (code && !user) {
		await supabase.auth.exchangeCodeForSession(code);
	}

	// May be able to do some cool promise thing where we pass down promises and
	// resolve them where needed, awaiting here introduces load delay.
	// Applies to all the await api's here.
	const agents = await api
		.GET('/agents/', {
			params: {
				query: {
					profile_id: user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving agents for profile ${user.id}: ${e.detail}`);
				return [];
			}
			if (!d) {
				console.warn(`No data returned from agents`);
				return [];
			}
			if (d.length === 0) {
				console.info(`No agents found for profile ${user.id}`);
				return [];
			}
			return d;
		})
		.catch((e) => {
			console.error(`Error retrieving agents for profile ${user.id}: ${e}`);
			return [];
		});

    const publishedAgents = await api
        .GET('/agents/', {
            params: {
                query: {
                    published: true
                }
            }
        })
        .then(({ data: d, error: e }) => {
            if (e) {
                console.error(`Error retrieving published agents: ${e.detail}`);
                return [];
            }
            if (!d) {
                console.warn(`No data returned from published agents`);
                return [];
            }
            if (d.length === 0) {
                console.info(`No published agents found`);
                return [];
            }
            return d;
        })
        .catch((e) => {
            console.error(`Error retrieving published agents: ${e}`);
            return [];
        });

	const crews = await api
		.GET('/crews/', {
			params: {
				query: {
					profile_id: user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving crews: ${e.detail}`);
				return [];
			}
			if (!d) {
				console.warn(`No data returned from crews`);
				return [];
			}
			if (d.length === 0) {
				console.info(`No crews found for profile ${user.id}`);
				return [];
			}
			return d;
		})
		.catch((e) => {
			console.error(`Error retrieving crews for profile ${user.id}: ${e}`);
			return [];
		});

	const sessions = await api
		.GET('/sessions/', {
			params: {
				query: {
					profile_id: user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving sessions for profile ${user.id}: ${e.detail}`);
				return [];
			}
			if (!d) {
				console.warn(`No data returned from sessions`);
				return [];
			}
			if (d.length === 0) {
				console.info(`No sessions found for profile ${user.id}`);
				return [];
			}
			return d;
		})
		.catch((e) => {
			console.error(`Error retrieving sessions for profile ${user.id}: ${e}`);
			return [];
		});

	const apiKeys = await api
		.GET('/api-keys/', {
			params: {
				query: {
					profile_id: user.id
				}
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error retrieving apiKeys for profile ${user.id}: ${e.detail}`);
				return [];
			}
			if (!d) {
				console.warn(`No data returned from apiKeys`);
				return [];
			}
			if (d.length === 0) {
				console.info(`No apiKeys found for profile ${user.id}`);
				return [];
			}
			return d;
		})
		.catch((e) => {
			console.error(`Error retrieving apiKeys for profile ${user.id}: ${e}`);
			return [];
		});

	const forms = {
		agent: {
			sv: await superValidate(zod(agentSchema))
		},
		crew: {
			sv: await superValidate(zod(crewSchema))
		}
	};

	return {
		user,
		agents,
        publishedAgents,
		crews,
		sessions,
		apiKeys,
		forms
	};
};
