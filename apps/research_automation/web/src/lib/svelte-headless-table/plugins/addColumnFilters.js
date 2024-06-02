import { keyed } from 'svelte-keyed';
import { derived, writable } from 'svelte/store';
const getFilteredRows = (rows, filterValues, columnOptions) => {
	const $filteredRows = rows
		// Filter `subRows`
		.map((row) => {
			const { subRows } = row;
			if (subRows === undefined) {
				return row;
			}
			const filteredSubRows = getFilteredRows(subRows, filterValues, columnOptions);
			const clonedRow = row.clone();
			clonedRow.subRows = filteredSubRows;
			return clonedRow;
		})
		.filter((row) => {
			if ((row.subRows?.length ?? 0) !== 0) {
				return true;
			}
			for (const [columnId, columnOption] of Object.entries(columnOptions)) {
				const bodyCell = row.cellForId[columnId];
				if (!bodyCell.isData()) {
					continue;
				}
				const { value } = bodyCell;
				const filterValue = filterValues[columnId];
				if (filterValue === undefined) {
					continue;
				}
				const isMatch = columnOption.fn({ value, filterValue });
				if (!isMatch) {
					return false;
				}
			}
			return true;
		});
	return $filteredRows;
};
export const addColumnFilters =
	({ serverSide = false } = {}) =>
	({ columnOptions, tableState }) => {
		const filterValues = writable({});
		const preFilteredRows = writable([]);
		const filteredRows = writable([]);
		const pluginState = { filterValues, preFilteredRows };
		const deriveRows = (rows) => {
			return derived([rows, filterValues], ([$rows, $filterValues]) => {
				preFilteredRows.set($rows);
				if (serverSide) {
					filteredRows.set($rows);
					return $rows;
				}
				const _filteredRows = getFilteredRows($rows, $filterValues, columnOptions);
				filteredRows.set(_filteredRows);
				return _filteredRows;
			});
		};
		return {
			pluginState,
			deriveRows,
			hooks: {
				'thead.tr.th': (headerCell) => {
					const filterValue = keyed(filterValues, headerCell.id);
					const props = derived([], () => {
						const columnOption = columnOptions[headerCell.id];
						if (columnOption === undefined) {
							return undefined;
						}
						filterValue.set(columnOption.initialFilterValue);
						const preFilteredValues = derived(preFilteredRows, ($rows) => {
							if (headerCell.isData()) {
								return $rows.map((row) => {
									// TODO check and handle different BodyCell types
									const cell = row.cellForId[headerCell.id];
									return cell?.value;
								});
							}
							return [];
						});
						const values = derived(filteredRows, ($rows) => {
							if (headerCell.isData()) {
								return $rows.map((row) => {
									// TODO check and handle different BodyCell types
									const cell = row.cellForId[headerCell.id];
									return cell?.value;
								});
							}
							return [];
						});
						const render = columnOption.render?.({
							id: headerCell.id,
							filterValue,
							...tableState,
							values,
							preFilteredRows,
							preFilteredValues
						});
						return { render };
					});
					return { props };
				}
			}
		};
	};
export const matchFilter = ({ filterValue, value }) => {
	if (filterValue === undefined) {
		return true;
	}
	return filterValue === value;
};
export const textPrefixFilter = ({ filterValue, value }) => {
	if (filterValue === '') {
		return true;
	}
	return String(value).toLowerCase().startsWith(String(filterValue).toLowerCase());
};
export const numberRangeFilter = ({ filterValue: [min, max], value }) => {
	return (min ?? -Infinity) <= value && value <= (max ?? Infinity);
};
