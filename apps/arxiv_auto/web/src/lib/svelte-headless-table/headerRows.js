import { derived } from 'svelte/store';
import {
	DataHeaderCell,
	FlatDisplayHeaderCell,
	GroupDisplayHeaderCell,
	GroupHeaderCell
} from './headerCells.js';
import { TableComponent } from './tableComponent.js';
import { sum } from './utils/math.js';
import { getNullMatrix, getTransposed } from './utils/matrix.js';
export class HeaderRow extends TableComponent {
	cells;
	constructor({ id, cells }) {
		super({ id });
		this.cells = cells;
	}
	attrs() {
		return derived(super.attrs(), ($baseAttrs) => {
			return {
				...$baseAttrs,
				role: 'row'
			};
		});
	}
	clone() {
		return new HeaderRow({
			id: this.id,
			cells: this.cells
		});
	}
}
export const getHeaderRows = (columns, flatColumnIds = []) => {
	const rowMatrix = getHeaderRowMatrix(columns);
	// Perform all column operations on the transposed columnMatrix. This helps
	// to reduce the number of expensive transpose operations required.
	let columnMatrix = getTransposed(rowMatrix);
	columnMatrix = getOrderedColumnMatrix(columnMatrix, flatColumnIds);
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	populateGroupHeaderCellIds(columnMatrix);
	return headerRowsForRowMatrix(getTransposed(columnMatrix));
};
export const getHeaderRowMatrix = (columns) => {
	const maxColspan = sum(columns.map((c) => (c.isGroup() ? c.ids.length : 1)));
	const maxHeight = Math.max(...columns.map((c) => c.height));
	const rowMatrix = getNullMatrix(maxColspan, maxHeight);
	let cellOffset = 0;
	columns.forEach((c) => {
		const heightOffset = maxHeight - c.height;
		loadHeaderRowMatrix(rowMatrix, c, heightOffset, cellOffset);
		cellOffset += c.isGroup() ? c.ids.length : 1;
	});
	// Replace null cells with blank display cells.
	return rowMatrix.map((cells, rowIdx) =>
		cells.map((cell, columnIdx) => {
			if (cell !== null) return cell;
			if (rowIdx === maxHeight - 1)
				return new FlatDisplayHeaderCell({ id: columnIdx.toString(), colstart: columnIdx });
			const flatId = rowMatrix[maxHeight - 1][columnIdx]?.id ?? columnIdx.toString();
			return new GroupDisplayHeaderCell({ ids: [], allIds: [flatId], colstart: columnIdx });
		})
	);
};
const loadHeaderRowMatrix = (rowMatrix, column, rowOffset, cellOffset) => {
	if (column.isData()) {
		// `DataHeaderCell` should always be in the last row.
		rowMatrix[rowMatrix.length - 1][cellOffset] = new DataHeaderCell({
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			label: column.header,
			accessorFn: column.accessorFn,
			accessorKey: column.accessorKey,
			id: column.id,
			colstart: cellOffset
		});
		return;
	}
	if (column.isDisplay()) {
		rowMatrix[rowMatrix.length - 1][cellOffset] = new FlatDisplayHeaderCell({
			id: column.id,
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			label: column.header,
			colstart: cellOffset
		});
		return;
	}
	if (column.isGroup()) {
		// Fill multi-colspan cells.
		for (let i = 0; i < column.ids.length; i++) {
			rowMatrix[rowOffset][cellOffset + i] = new GroupHeaderCell({
				// eslint-disable-next-line @typescript-eslint/no-explicit-any
				label: column.header,
				colspan: 1,
				allIds: column.ids,
				ids: [],
				colstart: cellOffset
			});
		}
		let childCellOffset = 0;
		column.columns.forEach((c) => {
			loadHeaderRowMatrix(rowMatrix, c, rowOffset + 1, cellOffset + childCellOffset);
			childCellOffset += c.isGroup() ? c.ids.length : 1;
		});
		return;
	}
};
export const getOrderedColumnMatrix = (columnMatrix, flatColumnIds) => {
	if (flatColumnIds.length === 0) {
		return columnMatrix;
	}
	const orderedColumnMatrix = [];
	// Each row of the transposed matrix represents a column.
	// The `FlatHeaderCell` should be the last cell of each column.
	flatColumnIds.forEach((key, columnIdx) => {
		const nextColumn = columnMatrix.find((columnCells) => {
			const flatCell = columnCells[columnCells.length - 1];
			if (!flatCell.isFlat()) {
				throw new Error('The last element of each column must be a `FlatHeaderCell`');
			}
			return flatCell.id === key;
		});
		if (nextColumn !== undefined) {
			orderedColumnMatrix.push(
				nextColumn.map((column) => {
					const clonedColumn = column.clone();
					clonedColumn.colstart = columnIdx;
					return clonedColumn;
				})
			);
		}
	});
	return orderedColumnMatrix;
};
const populateGroupHeaderCellIds = (columnMatrix) => {
	columnMatrix.forEach((columnCells) => {
		const lastCell = columnCells[columnCells.length - 1];
		if (!lastCell.isFlat()) {
			throw new Error('The last element of each column must be a `FlatHeaderCell`');
		}
		columnCells.forEach((c) => {
			if (c.isGroup()) {
				c.pushId(lastCell.id);
			}
		});
	});
};
export const headerRowsForRowMatrix = (rowMatrix) => {
	return rowMatrix.map((rowCells, rowIdx) => {
		return new HeaderRow({ id: rowIdx.toString(), cells: getMergedRow(rowCells) });
	});
};
/**
 * Multi-colspan cells will appear as multiple adjacent cells on the same row.
 * Join these adjacent multi-colspan cells and update the colspan property.
 *
 * Non-adjacent multi-colspan cells (due to column ordering) must be cloned
 * from the original .
 *
 * @param cells An array of cells.
 * @returns An array of cells with no duplicate consecutive cells.
 */
export const getMergedRow = (cells) => {
	if (cells.length === 0) {
		return cells;
	}
	const mergedCells = [];
	let startIdx = 0;
	let endIdx = 1;
	while (startIdx < cells.length) {
		const cell = cells[startIdx].clone();
		if (!cell.isGroup()) {
			mergedCells.push(cell);
			startIdx++;
			continue;
		}
		endIdx = startIdx + 1;
		const ids = [...cell.ids];
		while (endIdx < cells.length) {
			const nextCell = cells[endIdx];
			if (!nextCell.isGroup()) {
				break;
			}
			if (cell.allId !== nextCell.allId) {
				break;
			}
			ids.push(...nextCell.ids);
			endIdx++;
		}
		cell.setIds(ids);
		cell.colspan = endIdx - startIdx;
		mergedCells.push(cell);
		startIdx = endIdx;
	}
	return mergedCells;
};
