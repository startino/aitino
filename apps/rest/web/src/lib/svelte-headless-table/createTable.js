import { DataColumn, DisplayColumn, getFlatColumnIds, GroupColumn } from './columns.js';
import { getDuplicates } from './utils/array.js';
import { createViewModel } from './createViewModel.js';
export class Table {
	data;
	plugins;
	constructor(data, plugins) {
		this.data = data;
		this.plugins = plugins;
	}
	createColumns(columns) {
		const ids = getFlatColumnIds(columns);
		const duplicateIds = getDuplicates(ids);
		if (duplicateIds.length !== 0) {
			throw new Error(`Duplicate column ids not allowed: "${duplicateIds.join('", "')}"`);
		}
		return columns;
	}
	column(def) {
		return new DataColumn(def);
	}
	group(def) {
		return new GroupColumn(def);
	}
	display(def) {
		return new DisplayColumn(def);
	}
	createViewModel(columns, options) {
		return createViewModel(this, columns, options);
	}
}
export const createTable = (
	data,
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	plugins = {}
) => {
	return new Table(data, plugins);
};
