import { resolve } from 'node:path';

const project = resolve(process.cwd(), 'tsconfig.json');

/** @type {import("eslint").Linter.Config} */
module.exports = {
	extends: [
		'eslint:recommended',
		'prettier',
		'plugin:@typescript-eslint/recommended',
		'plugin:svelte/recommended',
		require.resolve('@vercel/style-guide/eslint/typescript'),
		'eslint-config-turbo'
	],
	plugins: ['only-warn'],
	globals: {
		Svelte: true
	},
	env: {
		node: true
	},
	settings: {
		'import/resolver': {
			typescript: {
				project
			}
		}
	},
	overrides: [
		{
			files: ['*.svelte'],
			parser: 'svelte-eslint-parser',
			// Parse the `<script>` in `.svelte` as TypeScript by adding the following configuration.
			parserOptions: {
				parser: '@typescript-eslint/parser'
			}
		}
	],
	ignorePatterns: ['node_modules/', '.svelte-kit/', '.vercel/', 'build/', 'dist/', 'out/']
};
