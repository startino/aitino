import { compare } from '../utils/compare.js';
import { isShiftClick } from '../utils/event.js';
import { derived, writable } from 'svelte/store';
const DEFAULT_TOGGLE_ORDER = ['asc', 'desc', undefined];
export const createSortKeysStore = (initKeys) => {
	const { subscribe, update, set } = writable(initKeys);
	const toggleId = (id, { multiSort = true, toggleOrder = DEFAULT_TOGGLE_ORDER } = {}) => {
		update(($sortKeys) => {
			const keyIdx = $sortKeys.findIndex((key) => key.id === id);
			const key = $sortKeys[keyIdx];
			const order = key?.order;
			const orderIdx = toggleOrder.findIndex((o) => o === order);
			const nextOrderIdx = (orderIdx + 1) % toggleOrder.length;
			const nextOrder = toggleOrder[nextOrderIdx];
			if (!multiSort) {
				if (nextOrder === undefined) {
					return [];
				}
				return [{ id, order: nextOrder }];
			}
			if (keyIdx === -1 && nextOrder !== undefined) {
				return [...$sortKeys, { id, order: nextOrder }];
			}
			if (nextOrder === undefined) {
				return [...$sortKeys.slice(0, keyIdx), ...$sortKeys.slice(keyIdx + 1)];
			}
			return [
				...$sortKeys.slice(0, keyIdx),
				{ id, order: nextOrder },
				...$sortKeys.slice(keyIdx + 1)
			];
		});
	};
	const clearId = (id) => {
		update(($sortKeys) => {
			const keyIdx = $sortKeys.findIndex((key) => key.id === id);
			if (keyIdx === -1) {
				return $sortKeys;
			}
			return [...$sortKeys.slice(0, keyIdx), ...$sortKeys.slice(keyIdx + 1)];
		});
	};
	return {
		subscribe,
		update,
		set,
		toggleId,
		clearId
	};
};
const getSortedRows = (rows, sortKeys, columnOptions) => {
	// Shallow clone to prevent sort affecting `preSortedRows`.
	const $sortedRows = [...rows];
	$sortedRows.sort((a, b) => {
		for (const key of sortKeys) {
			const invert = columnOptions[key.id]?.invert ?? false;
			// TODO check why cellForId returns `undefined`.
			const cellA = a.cellForId[key.id];
			const cellB = b.cellForId[key.id];
			let order = 0;
			const compareFn = columnOptions[key.id]?.compareFn;
			const getSortValue = columnOptions[key.id]?.getSortValue;
			// Only need to check properties of `cellA` as both should have the same
			// properties.
			if (!cellA.isData()) {
				return 0;
			}
			const valueA = cellA.value;
			const valueB = cellB.value;
			if (compareFn !== undefined) {
				order = compareFn(valueA, valueB);
			} else if (getSortValue !== undefined) {
				const sortValueA = getSortValue(valueA);
				const sortValueB = getSortValue(valueB);
				order = compare(sortValueA, sortValueB);
			} else if (typeof valueA === 'string' || typeof valueA === 'number') {
				// typeof `cellB.value` is logically equal to `cellA.value`.
				order = compare(valueA, valueB);
			} else if (valueA instanceof Date || valueB instanceof Date) {
				const sortValueA = valueA instanceof Date ? valueA.getTime() : 0;
				const sortValueB = valueB instanceof Date ? valueB.getTime() : 0;
				order = compare(sortValueA, sortValueB);
			}
			if (order !== 0) {
				let orderFactor = 1;
				// If the current key order is `'desc'`, reverse the order.
				if (key.order === 'desc') {
					orderFactor *= -1;
				}
				// If `invert` is `true`, we want to invert the sort without
				// affecting the view model's indication.
				if (invert) {
					orderFactor *= -1;
				}
				return order * orderFactor;
			}
		}
		return 0;
	});
	for (let i = 0; i < $sortedRows.length; i++) {
		const { subRows } = $sortedRows[i];
		if (subRows === undefined) {
			continue;
		}
		const sortedSubRows = getSortedRows(subRows, sortKeys, columnOptions);
		const clonedRow = $sortedRows[i].clone();
		clonedRow.subRows = sortedSubRows;
		$sortedRows[i] = clonedRow;
	}
	return $sortedRows;
};
export const addSortBy =
	({
		initialSortKeys = [],
		disableMultiSort = false,
		isMultiSortEvent = isShiftClick,
		toggleOrder,
		serverSide = false
	} = {}) =>
	({ columnOptions }) => {
		const disabledSortIds = Object.entries(columnOptions)
			.filter(([, option]) => option.disable === true)
			.map(([columnId]) => columnId);
		const sortKeys = createSortKeysStore(initialSortKeys);
		const preSortedRows = writable([]);
		const deriveRows = (rows) => {
			return derived([rows, sortKeys], ([$rows, $sortKeys]) => {
				preSortedRows.set($rows);
				if (serverSide) {
					return $rows;
				}
				return getSortedRows($rows, $sortKeys, columnOptions);
			});
		};
		const pluginState = { sortKeys, preSortedRows };
		return {
			pluginState,
			deriveRows,
			hooks: {
				'thead.tr.th': (cell) => {
					const disabled = disabledSortIds.includes(cell.id);
					const props = derived(sortKeys, ($sortKeys) => {
						const key = $sortKeys.find((k) => k.id === cell.id);
						const toggle = (event) => {
							if (!cell.isData()) return;
							if (disabled) return;
							sortKeys.toggleId(cell.id, {
								multiSort: disableMultiSort ? false : isMultiSortEvent(event),
								toggleOrder
							});
						};
						const clear = () => {
							if (!cell.isData()) return;
							if (disabledSortIds.includes(cell.id)) return;
							sortKeys.clearId(cell.id);
						};
						return {
							order: key?.order,
							toggle,
							clear,
							disabled
						};
					});
					return { props };
				},
				'tbody.tr.td': (cell) => {
					const props = derived(sortKeys, ($sortKeys) => {
						const key = $sortKeys.find((k) => k.id === cell.id);
						return {
							order: key?.order
						};
					});
					return { props };
				}
			}
		};
	};
