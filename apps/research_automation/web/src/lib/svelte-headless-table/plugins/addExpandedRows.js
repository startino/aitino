import { recordSetStore } from '../utils/store.js';
import { keyed } from 'svelte-keyed';
import { derived, readable } from 'svelte/store';
const withExpandedRows = (row, expandedIds) => {
	if (row.subRows === undefined) {
		return [row];
	}
	if (expandedIds[row.id] !== true) {
		return [row];
	}
	const expandedSubRows = row.subRows.flatMap((subRow) => withExpandedRows(subRow, expandedIds));
	return [row, ...expandedSubRows];
};
export const addExpandedRows =
	({ initialExpandedIds = {} } = {}) =>
	() => {
		const expandedIds = recordSetStore(initialExpandedIds);
		const getRowState = (row) => {
			const isExpanded = keyed(expandedIds, row.id);
			const canExpand = readable((row.subRows?.length ?? 0) > 0);
			const subRowExpandedIds = derived(expandedIds, ($expandedIds) => {
				// Check prefix with '>' to match child ids while ignoring this row's id.
				return Object.entries($expandedIds).filter(
					([id, expanded]) => id.startsWith(`${row.id}>`) && expanded
				);
			});
			// If the number of expanded subRows is equal to the number of subRows
			// that can expand, then all subRows are expanded.
			const isAllSubRowsExpanded = derived(subRowExpandedIds, ($subRowExpandedIds) => {
				if (row.subRows === undefined) {
					return true;
				}
				// canExpand is derived from the presence of the `subRows` property.
				const expandableSubRows = row.subRows.filter((subRow) => subRow.subRows !== undefined);
				return $subRowExpandedIds.length === expandableSubRows.length;
			});
			return {
				isExpanded,
				canExpand,
				isAllSubRowsExpanded
			};
		};
		const pluginState = { expandedIds, getRowState };
		const deriveRows = (rows) => {
			return derived([rows, expandedIds], ([$rows, $expandedIds]) => {
				return $rows.flatMap((row) => {
					return withExpandedRows(row, $expandedIds);
				});
			});
		};
		return {
			pluginState,
			deriveRows
		};
	};
