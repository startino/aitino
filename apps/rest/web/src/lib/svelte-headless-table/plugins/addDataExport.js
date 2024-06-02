import { isReadable } from '../utils/store.js';
import { derived, get } from 'svelte/store';
const getObjectsFromRows = (rows, ids, childrenKey) => {
	return rows.map((row) => {
		const dataObject = Object.fromEntries(
			ids.map((id) => {
				const cell = row.cellForId[id];
				if (cell.isData()) {
					return [id, cell.value];
				}
				if (cell.isDisplay() && cell.column.data !== undefined) {
					// eslint-disable-next-line @typescript-eslint/no-explicit-any
					let data = cell.column.data(cell, row.state);
					if (isReadable(data)) {
						data = get(data);
					}
					return [id, data];
				}
				return [id, null];
			})
		);
		if (row.subRows !== undefined) {
			dataObject[childrenKey] = getObjectsFromRows(row.subRows, ids, childrenKey);
		}
		return dataObject;
	});
};
const getCsvFromRows = (rows, ids) => {
	const dataLines = rows.map((row) => {
		const line = ids.map((id) => {
			const cell = row.cellForId[id];
			if (cell.isData()) {
				return cell.value;
			}
			if (cell.isDisplay() && cell.column.data !== undefined) {
				// eslint-disable-next-line @typescript-eslint/no-explicit-any
				let data = cell.column.data(cell, row.state);
				if (isReadable(data)) {
					data = get(data);
				}
				return data;
			}
			return null;
		});
		return line.join(',');
	});
	const headerLine = ids.join(',');
	return headerLine + '\n' + dataLines.join('\n');
};
export const addDataExport =
	({ format = 'object', childrenKey = 'children' } = {}) =>
	({ tableState, columnOptions }) => {
		const excludedIds = Object.entries(columnOptions)
			.filter(([, option]) => option.exclude === true)
			.map(([columnId]) => columnId);
		const { visibleColumns, rows } = tableState;
		const exportedIds = derived(visibleColumns, ($visibleColumns) =>
			$visibleColumns.map((c) => c.id).filter((id) => !excludedIds.includes(id))
		);
		const exportedData = derived([rows, exportedIds], ([$rows, $exportedIds]) => {
			switch (format) {
				case 'json':
					return JSON.stringify(getObjectsFromRows($rows, $exportedIds, childrenKey));
				case 'csv':
					return getCsvFromRows($rows, $exportedIds);
				default:
					return getObjectsFromRows($rows, $exportedIds, childrenKey);
			}
		});
		const pluginState = { exportedData };
		return {
			pluginState
		};
	};
