import { derived, writable } from 'svelte/store';
export const addHiddenColumns =
	({ initialHiddenColumnIds = [] } = {}) =>
	() => {
		const hiddenColumnIds = writable(initialHiddenColumnIds);
		const pluginState = { hiddenColumnIds };
		const deriveFlatColumns = (flatColumns) => {
			return derived([flatColumns, hiddenColumnIds], ([$flatColumns, $hiddenColumnIds]) => {
				if ($hiddenColumnIds.length === 0) {
					return $flatColumns;
				}
				return $flatColumns.filter((c) => !$hiddenColumnIds.includes(c.id));
			});
		};
		return {
			pluginState,
			deriveFlatColumns
		};
	};
