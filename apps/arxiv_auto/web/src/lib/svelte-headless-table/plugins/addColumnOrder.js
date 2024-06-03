import { derived, writable } from 'svelte/store';
export const addColumnOrder =
	({ initialColumnIdOrder = [], hideUnspecifiedColumns = false } = {}) =>
	() => {
		const columnIdOrder = writable(initialColumnIdOrder);
		const pluginState = { columnIdOrder };
		const deriveFlatColumns = (flatColumns) => {
			return derived([flatColumns, columnIdOrder], ([$flatColumns, $columnIdOrder]) => {
				const _flatColumns = [...$flatColumns];
				const orderedFlatColumns = [];
				$columnIdOrder.forEach((id) => {
					const colIdx = _flatColumns.findIndex((c) => c.id === id);
					orderedFlatColumns.push(..._flatColumns.splice(colIdx, 1));
				});
				if (!hideUnspecifiedColumns) {
					// Push the remaining unspecified columns.
					orderedFlatColumns.push(..._flatColumns);
				}
				return orderedFlatColumns;
			});
		};
		return {
			pluginState,
			deriveFlatColumns
		};
	};
