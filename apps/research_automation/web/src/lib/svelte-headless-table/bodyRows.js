import { derived } from 'svelte/store';
import { BodyCell, DataBodyCell, DisplayBodyCell } from './bodyCells.js';
import { TableComponent } from './tableComponent.js';
import { nonUndefined } from './utils/filter.js';
export class BodyRow extends TableComponent {
	cells;
	/**
	 * Get the cell with a given column id.
	 *
	 * **This includes hidden cells.**
	 */
	cellForId;
	depth;
	parentRow;
	subRows;
	constructor({ id, cells, cellForId, depth = 0, parentRow }) {
		super({ id });
		this.cells = cells;
		this.cellForId = cellForId;
		this.depth = depth;
		this.parentRow = parentRow;
	}
	attrs() {
		return derived(super.attrs(), ($baseAttrs) => {
			return {
				...$baseAttrs,
				role: 'row'
			};
		});
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isData() {
		return '__data' in this;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isDisplay() {
		return '__display' in this;
	}
}
export class DataBodyRow extends BodyRow {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__data = true;
	dataId;
	original;
	constructor({ id, dataId, original, cells, cellForId, depth = 0, parentRow }) {
		super({ id, cells, cellForId, depth, parentRow });
		this.dataId = dataId;
		this.original = original;
	}
	clone({ includeCells = false, includeSubRows = false } = {}) {
		const clonedRow = new DataBodyRow({
			id: this.id,
			dataId: this.dataId,
			cellForId: this.cellForId,
			cells: this.cells,
			original: this.original,
			depth: this.depth
		});
		if (includeCells) {
			const clonedCellsForId = Object.fromEntries(
				Object.entries(clonedRow.cellForId).map(([id, cell]) => {
					const clonedCell = cell.clone();
					clonedCell.row = clonedRow;
					return [id, clonedCell];
				})
			);
			const clonedCells = clonedRow.cells.map(({ id }) => clonedCellsForId[id]);
			clonedRow.cellForId = clonedCellsForId;
			clonedRow.cells = clonedCells;
		}
		if (includeSubRows) {
			const clonedSubRows = this.subRows?.map((row) => row.clone({ includeCells, includeSubRows }));
			clonedRow.subRows = clonedSubRows;
		} else {
			clonedRow.subRows = this.subRows;
		}
		return clonedRow;
	}
}
export class DisplayBodyRow extends BodyRow {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__display = true;
	constructor({ id, cells, cellForId, depth = 0, parentRow }) {
		super({ id, cells, cellForId, depth, parentRow });
	}
	clone({ includeCells = false, includeSubRows = false } = {}) {
		const clonedRow = new DisplayBodyRow({
			id: this.id,
			cellForId: this.cellForId,
			cells: this.cells,
			depth: this.depth
		});
		clonedRow.subRows = this.subRows;
		if (includeCells) {
			const clonedCellsForId = Object.fromEntries(
				Object.entries(clonedRow.cellForId).map(([id, cell]) => {
					const clonedCell = cell.clone();
					clonedCell.row = clonedRow;
					return [id, clonedCell];
				})
			);
			const clonedCells = clonedRow.cells.map(({ id }) => clonedCellsForId[id]);
			clonedRow.cellForId = clonedCellsForId;
			clonedRow.cells = clonedCells;
		}
		if (includeSubRows) {
			const clonedSubRows = this.subRows?.map((row) => row.clone({ includeCells, includeSubRows }));
			clonedRow.subRows = clonedSubRows;
		} else {
			clonedRow.subRows = this.subRows;
		}
		return clonedRow;
	}
}
/**
 * Converts an array of items into an array of table `BodyRow`s based on the column structure.
 * @param data The data to display.
 * @param flatColumns The column structure.
 * @returns An array of `BodyRow`s representing the table structure.
 */
export const getBodyRows = (
	data,
	/**
	 * Flat columns before column transformations.
	 */
	flatColumns,
	{ rowDataId } = {}
) => {
	const rows = data.map((item, idx) => {
		const id = idx.toString();
		return new DataBodyRow({
			id,
			dataId: rowDataId !== undefined ? rowDataId(item, idx) : id,
			original: item,
			cells: [],
			cellForId: {}
		});
	});
	data.forEach((item, rowIdx) => {
		const cells = flatColumns.map((col) => {
			if (col.isData()) {
				const dataCol = col;
				const value = dataCol.getValue(item);
				return new DataBodyCell({
					row: rows[rowIdx],
					column: dataCol,
					label: col.cell,
					value
				});
			}
			if (col.isDisplay()) {
				const displayCol = col;
				return new DisplayBodyCell({
					row: rows[rowIdx],
					column: displayCol,
					label: col.cell
				});
			}
			throw new Error('Unrecognized `FlatColumn` implementation');
		});
		rows[rowIdx].cells = cells;
		flatColumns.forEach((c, colIdx) => {
			rows[rowIdx].cellForId[c.id] = cells[colIdx];
		});
	});
	return rows;
};
/**
 * Arranges and hides columns in an array of `BodyRow`s based on
 * `columnIdOrder` by transforming the `cells` property of each row.
 *
 * `cellForId` should remain unaffected.
 *
 * @param rows The rows to transform.
 * @param columnIdOrder The column order to transform to.
 * @returns A new array of `BodyRow`s with corrected row references.
 */
export const getColumnedBodyRows = (rows, columnIdOrder) => {
	const columnedRows = rows.map((row) => {
		const clonedRow = row.clone();
		clonedRow.cells = [];
		clonedRow.cellForId = {};
		return clonedRow;
	});
	if (rows.length === 0 || columnIdOrder.length === 0) return rows;
	rows.forEach((row, rowIdx) => {
		// Create a shallow copy of `row.cells` to reassign each `cell`'s `row`
		// reference.
		const cells = row.cells.map((cell) => {
			const clonedCell = cell.clone();
			clonedCell.row = columnedRows[rowIdx];
			return clonedCell;
		});
		const visibleCells = columnIdOrder
			.map((cid) => {
				return cells.find((c) => c.id === cid);
			})
			.filter(nonUndefined);
		columnedRows[rowIdx].cells = visibleCells;
		// Include hidden cells in `cellForId` to allow row transformations on
		// hidden cells.
		cells.forEach((cell) => {
			columnedRows[rowIdx].cellForId[cell.id] = cell;
		});
	});
	return columnedRows;
};
/**
 * Converts an array of items into an array of table `BodyRow`s based on a parent row.
 * @param subItems The sub data to display.
 * @param parentRow The parent row.
 * @returns An array of `BodyRow`s representing the child rows of `parentRow`.
 */
export const getSubRows = (subItems, parentRow, { rowDataId } = {}) => {
	const subRows = subItems.map((item, idx) => {
		const id = `${parentRow.id}>${idx}`;
		return new DataBodyRow({
			id,
			dataId: rowDataId !== undefined ? rowDataId(item, idx) : id,
			original: item,
			cells: [],
			cellForId: {},
			depth: parentRow.depth + 1,
			parentRow
		});
	});
	subItems.forEach((item, rowIdx) => {
		// parentRow.cells only include visible cells.
		// We have to derive all cells from parentRow.cellForId
		const cellForId = Object.fromEntries(
			Object.values(parentRow.cellForId).map((cell) => {
				const { column } = cell;
				if (column.isData()) {
					const dataCol = column;
					const value = dataCol.getValue(item);
					return [
						column.id,
						new DataBodyCell({ row: subRows[rowIdx], column, label: column.cell, value })
					];
				}
				if (column.isDisplay()) {
					return [
						column.id,
						new DisplayBodyCell({ row: subRows[rowIdx], column, label: column.cell })
					];
				}
				throw new Error('Unrecognized `FlatColumn` implementation');
			})
		);
		subRows[rowIdx].cellForId = cellForId;
		const cells = parentRow.cells.map((cell) => {
			return cellForId[cell.id];
		});
		subRows[rowIdx].cells = cells;
	});
	return subRows;
};
