import { DataBodyRow, getSubRows } from '../bodyRows.js';
import { derived } from 'svelte/store';
const withSubRows = (row, getChildren) => {
	const subItems = getChildren(row.original);
	if (subItems === undefined) {
		return row;
	}
	const subRows = getSubRows(subItems, row);
	row.subRows = subRows.map((row) => withSubRows(row, getChildren));
	return row;
};
export const addSubRows =
	({ children }) =>
	() => {
		const getChildren = children instanceof Function ? children : (item) => item[children];
		const deriveRows = (rows) => {
			return derived(rows, ($rows) => {
				return $rows.map((row) => {
					if (row.isData()) {
						return withSubRows(row, getChildren);
					}
					return row;
				});
			});
		};
		return {
			pluginState: {},
			deriveRows
		};
	};
