import { DataBodyCell } from '../bodyCells.js';
import { BodyRow, DisplayBodyRow } from '../bodyRows.js';
import { isShiftClick } from '../utils/event.js';
import { nonUndefined } from '../utils/filter.js';
import { arraySetStore } from '../utils/store.js';
import { derived, writable } from 'svelte/store';
const getIdPrefix = (id) => {
	const prefixTokens = id.split('>').slice(0, -1);
	if (prefixTokens.length === 0) {
		return '';
	}
	return `${prefixTokens.join('>')}>`;
};
const getIdLeaf = (id) => {
	const tokens = id.split('>');
	return tokens[tokens.length - 1] ?? '';
};
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const deepenIdAndDepth = (row, parentId) => {
	row.id = `${parentId}>${row.id}`;
	row.depth = row.depth + 1;
	row.subRows?.forEach((subRow) => deepenIdAndDepth(subRow, parentId));
};
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getGroupedRows = (
	rows,
	groupByIds,
	columnOptions,
	{ repeatCellIds, aggregateCellIds, groupCellIds, allGroupByIds }
) => {
	if (groupByIds.length === 0) {
		return rows;
	}
	if (rows.length === 0) {
		return rows;
	}
	const idPrefix = getIdPrefix(rows[0].id);
	const [groupById, ...restIds] = groupByIds;
	const subRowsForGroupOnValue = new Map();
	for (const row of rows) {
		const cell = row.cellForId[groupById];
		if (!cell.isData()) {
			break;
		}
		const columnOption = columnOptions[groupById] ?? {};
		const { getGroupOn } = columnOption;
		const groupOnValue = getGroupOn?.(cell.value) ?? cell.value;
		if (typeof groupOnValue === 'function' || typeof groupOnValue === 'object') {
			console.warn(
				`Missing \`getGroupOn\` column option to aggregate column "${groupById}" with object values`
			);
		}
		const subRows = subRowsForGroupOnValue.get(groupOnValue) ?? [];
		subRowsForGroupOnValue.set(groupOnValue, [...subRows, row]);
	}
	const groupedRows = [];
	let groupRowIdx = 0;
	for (const [groupOnValue, subRows] of subRowsForGroupOnValue.entries()) {
		// Guaranteed to have at least one subRow.
		const firstRow = subRows[0];
		const groupRow = new DisplayBodyRow({
			id: `${idPrefix}${groupRowIdx++}`,
			// TODO Differentiate data rows and grouped rows.
			depth: firstRow.depth,
			cells: [],
			cellForId: {}
		});
		const groupRowCellForId = Object.fromEntries(
			Object.entries(firstRow.cellForId).map(([id, cell]) => {
				if (id === groupById) {
					const newCell = new DataBodyCell({
						column: cell.column,
						row: groupRow,
						value: groupOnValue
					});
					return [id, newCell];
				}
				const columnCells = subRows.map((row) => row.cellForId[id]).filter(nonUndefined);
				if (!columnCells[0].isData()) {
					const clonedCell = columnCells[0].clone();
					clonedCell.row = groupRow;
					return [id, clonedCell];
				}
				const { cell: label, getAggregateValue } = columnOptions[id] ?? {};
				const columnValues = columnCells.map((cell) => cell.value);
				const value = getAggregateValue === undefined ? '' : getAggregateValue(columnValues);
				const newCell = new DataBodyCell({
					column: cell.column,
					row: groupRow,
					value,
					label
				});
				return [id, newCell];
			})
		);
		const groupRowCells = firstRow.cells.map((cell) => {
			return groupRowCellForId[cell.id];
		});
		groupRow.cellForId = groupRowCellForId;
		groupRow.cells = groupRowCells;
		const groupRowSubRows = subRows.map((subRow) => {
			const clonedSubRow = subRow.clone({ includeCells: true, includeSubRows: true });
			deepenIdAndDepth(clonedSubRow, groupRow.id);
			return clonedSubRow;
		});
		groupRow.subRows = getGroupedRows(groupRowSubRows, restIds, columnOptions, {
			repeatCellIds,
			aggregateCellIds,
			groupCellIds,
			allGroupByIds
		});
		groupedRows.push(groupRow);
		groupRow.cells.forEach((cell) => {
			if (cell.id === groupById) {
				groupCellIds[cell.rowColId()] = true;
			} else {
				aggregateCellIds[cell.rowColId()] = true;
			}
		});
		groupRow.subRows.forEach((subRow) => {
			subRow.parentRow = groupRow;
			subRow.cells.forEach((cell) => {
				if (allGroupByIds.includes(cell.id) && groupCellIds[cell.rowColId()] !== true) {
					repeatCellIds[cell.rowColId()] = true;
				}
			});
		});
	}
	return groupedRows;
};
export const addGroupBy =
	({ initialGroupByIds = [], disableMultiGroup = false, isMultiGroupEvent = isShiftClick } = {}) =>
	({ columnOptions }) => {
		const disabledGroupIds = Object.entries(columnOptions)
			.filter(([, option]) => option.disable === true)
			.map(([columnId]) => columnId);
		const groupByIds = arraySetStore(initialGroupByIds);
		const repeatCellIds = writable({});
		const aggregateCellIds = writable({});
		const groupCellIds = writable({});
		const pluginState = {
			groupByIds
		};
		const deriveRows = (rows) => {
			return derived([rows, groupByIds], ([$rows, $groupByIds]) => {
				const $repeatCellIds = {};
				const $aggregateCellIds = {};
				const $groupCellIds = {};
				const $groupedRows = getGroupedRows($rows, $groupByIds, columnOptions, {
					repeatCellIds: $repeatCellIds,
					aggregateCellIds: $aggregateCellIds,
					groupCellIds: $groupCellIds,
					allGroupByIds: $groupByIds
				});
				repeatCellIds.set($repeatCellIds);
				aggregateCellIds.set($aggregateCellIds);
				groupCellIds.set($groupCellIds);
				return $groupedRows;
			});
		};
		return {
			pluginState,
			deriveRows,
			hooks: {
				'thead.tr.th': (cell) => {
					const disabled = disabledGroupIds.includes(cell.id) || !cell.isData();
					const props = derived(groupByIds, ($groupByIds) => {
						const grouped = $groupByIds.includes(cell.id);
						const toggle = (event) => {
							if (!cell.isData()) return;
							if (disabled) return;
							groupByIds.toggle(cell.id, {
								clearOthers: disableMultiGroup || !isMultiGroupEvent(event)
							});
						};
						const clear = () => {
							groupByIds.remove(cell.id);
						};
						return {
							grouped,
							toggle,
							clear,
							disabled
						};
					});
					return { props };
				},
				'tbody.tr.td': (cell) => {
					const props = derived(
						[repeatCellIds, aggregateCellIds, groupCellIds],
						([$repeatCellIds, $aggregateCellIds, $groupCellIds]) => {
							return {
								repeated: $repeatCellIds[cell.rowColId()] === true,
								aggregated: $aggregateCellIds[cell.rowColId()] === true,
								grouped: $groupCellIds[cell.rowColId()] === true
							};
						}
					);
					return { props };
				}
			}
		};
	};
