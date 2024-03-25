import * as dotenv from 'dotenv';
dotenv.config();

function getEnvironmentVariable(environmentVariable: string): string {
	const validEnvironmentVariable = process.env[environmentVariable];
	if (!validEnvironmentVariable) {
		throw new Error(`Couldn't find environment variable: ${environmentVariable}`);
	}
	return validEnvironmentVariable;
}

export const ENV = {
	PUBLIC_SUPABASE_ANON_KEY: getEnvironmentVariable('PUBLIC_SUPABASE_ANON_KEY'),
	PUBLIC_SUPABASE_URL: getEnvironmentVariable('PUBLIC_SUPABASE_URL'),
	SUPABASE_SERVICE_ROLE_KEY: getEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY'),
	SUPABASE_DB_URL: getEnvironmentVariable('SUPABASE_DB_URL'),
	STRIPE_SECRET_KEY: getEnvironmentVariable('STRIPE_SECRET_KEY'),
	STRIPE_SIGNING_SECRET: getEnvironmentVariable('STRIPE_SIGNING_SECRET'),
	PUBLIC_BASE_URL: getEnvironmentVariable('PUBLIC_BASE_URL')
};
