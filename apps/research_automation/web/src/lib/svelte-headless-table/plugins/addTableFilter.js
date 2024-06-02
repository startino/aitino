import { recordSetStore } from '../utils/store.js';
import { derived, writable } from 'svelte/store';
import { textPrefixFilter } from './addColumnFilters.js';
const getFilteredRows = (
	rows,
	filterValue,
	columnOptions,
	{ tableCellMatches, fn, includeHiddenColumns }
) => {
	const $filteredRows = rows
		// Filter `subRows`
		.map((row) => {
			const { subRows } = row;
			if (subRows === undefined) {
				return row;
			}
			const filteredSubRows = getFilteredRows(subRows, filterValue, columnOptions, {
				tableCellMatches,
				fn,
				includeHiddenColumns
			});
			const clonedRow = row.clone();
			clonedRow.subRows = filteredSubRows;
			return clonedRow;
		})
		.filter((row) => {
			if ((row.subRows?.length ?? 0) !== 0) {
				return true;
			}
			// An array of booleans, true if the cell matches the filter.
			const rowCellMatches = Object.values(row.cellForId).map((cell) => {
				const options = columnOptions[cell.id];
				if (options?.exclude === true) {
					return false;
				}
				const isHidden = row.cells.find((c) => c.id === cell.id) === undefined;
				if (isHidden && !includeHiddenColumns) {
					return false;
				}
				if (!cell.isData()) {
					return false;
				}
				let value = cell.value;
				if (options?.getFilterValue !== undefined) {
					value = options?.getFilterValue(value);
				}
				const matches = fn({ value: String(value), filterValue });
				if (matches) {
					const dataRowColId = cell.dataRowColId();
					if (dataRowColId !== undefined) {
						tableCellMatches[dataRowColId] = matches;
					}
				}
				return matches;
			});
			// If any cell matches, include in the filtered results.
			return rowCellMatches.includes(true);
		});
	return $filteredRows;
};
export const addTableFilter =
	({
		fn = textPrefixFilter,
		initialFilterValue = '',
		includeHiddenColumns = false,
		serverSide = false
	} = {}) =>
	({ columnOptions }) => {
		const filterValue = writable(initialFilterValue);
		const preFilteredRows = writable([]);
		const tableCellMatches = recordSetStore();
		const pluginState = { filterValue, preFilteredRows };
		const deriveRows = (rows) => {
			return derived([rows, filterValue], ([$rows, $filterValue]) => {
				preFilteredRows.set($rows);
				tableCellMatches.clear();
				const $tableCellMatches = {};
				const $filteredRows = getFilteredRows($rows, $filterValue, columnOptions, {
					tableCellMatches: $tableCellMatches,
					fn,
					includeHiddenColumns
				});
				tableCellMatches.set($tableCellMatches);
				if (serverSide) {
					return $rows;
				}
				return $filteredRows;
			});
		};
		return {
			pluginState,
			deriveRows,
			hooks: {
				'tbody.tr.td': (cell) => {
					const props = derived(
						[filterValue, tableCellMatches],
						([$filterValue, $tableCellMatches]) => {
							const dataRowColId = cell.dataRowColId();
							return {
								matches:
									$filterValue !== '' &&
									dataRowColId !== undefined &&
									($tableCellMatches[dataRowColId] ?? false)
							};
						}
					);
					return { props };
				}
			}
		};
	};
