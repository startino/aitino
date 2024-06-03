import { derived, writable } from 'svelte/store';
export const getFlattenedRows = (rows, depth) => {
	if (depth === 0) return rows;
	const flattenedRows = [];
	for (const row of rows) {
		if (row.subRows === undefined) continue;
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		flattenedRows.push(...getFlattenedRows(row.subRows, depth - 1));
	}
	return flattenedRows;
};
export const addFlatten =
	({ initialDepth = 0 } = {}) =>
	() => {
		const depth = writable(initialDepth);
		const pluginState = { depth };
		const deriveRows = (rows) => {
			return derived([rows, depth], ([$rows, $depth]) => {
				return getFlattenedRows($rows, $depth);
			});
		};
		return {
			pluginState,
			deriveRows,
			hooks: {
				'tbody.tr.td': () => {
					const props = derived([], () => {
						const flatten = ($depth) => {
							depth.set($depth);
						};
						const unflatten = () => flatten(0);
						return { flatten, unflatten };
					});
					return { props };
				}
			}
		};
	};
