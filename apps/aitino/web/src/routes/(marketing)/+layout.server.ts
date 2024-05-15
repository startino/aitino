import { serverGetSplitTestIdentifier } from 'svelte-split-testing';

export async function load({ cookies }) {
	const splitTestIdentifier = serverGetSplitTestIdentifier(cookies);

	return {
		splitTestIdentifier
	};
}
