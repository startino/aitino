export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13'),
	() => import('./nodes/14'),
	() => import('./nodes/15'),
	() => import('./nodes/16'),
	() => import('./nodes/17'),
	() => import('./nodes/18'),
	() => import('./nodes/19'),
	() => import('./nodes/20'),
	() => import('./nodes/21')
];

export const server_loads = [0,2,6];

export const dictionary = {
		"/(marketing)": [~8,[2]],
		"/app": [13,[6]],
		"/app/account": [14,[6]],
		"/app/auto-build": [15,[6]],
		"/app/editor/agent": [16,[6,7]],
		"/app/editor/crew": [~17,[6,7]],
		"/app/library": [18,[6]],
		"/app/library/agent": [19,[6]],
		"/app/library/crew": [20,[6]],
		"/app/sessions": [~21,[6]],
		"/(marketing)/blog": [~11,[2,4]],
		"/(marketing)/blog/(blog-article)/[slug]": [~12,[2,4,5]],
		"/(marketing)/(auth)/login": [~9,[2,3]],
		"/(marketing)/(auth)/register": [~10,[2,3]]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),

	reroute: (() => {})
};

export { default as root } from '../root.svelte';