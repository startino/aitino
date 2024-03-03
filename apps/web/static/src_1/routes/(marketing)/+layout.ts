export async function load({ data }) {
	const { splitTestIdentifier } = data || {};

	return {
		splitTestIdentifier
	};
}
