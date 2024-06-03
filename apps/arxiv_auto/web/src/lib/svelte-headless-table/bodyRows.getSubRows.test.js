import { writable } from 'svelte/store';
import { DataBodyCell, DisplayBodyCell } from './bodyCells.js';
import { BodyRow, DataBodyRow, getBodyRows, getColumnedBodyRows, getSubRows } from './bodyRows.js';
import { createTable } from './createTable.js';
const parentData = {
	firstName: 'Charlie',
	lastName: 'Brown',
	age: 30,
	progress: 75,
	status: 'completed',
	visits: 32
};
const data = [
	{
		firstName: 'Adam',
		lastName: 'West',
		age: 50,
		progress: 75,
		status: 'completed',
		visits: 32
	},
	{
		firstName: 'Becky',
		lastName: 'White',
		age: 93,
		progress: 43,
		status: 'completed',
		visits: 10
	}
];
const table = createTable(writable(data));
const dataColumns = [
	table.column({
		accessor: 'firstName',
		header: 'First Name'
	}),
	table.column({
		accessor: 'lastName',
		header: 'Last Name'
	}),
	table.column({
		accessor: 'progress',
		header: 'Profile Progress'
	})
];
const parentRow = getBodyRows([parentData], dataColumns)[0];
it('transforms empty data', () => {
	const actual = getSubRows([], parentRow);
	const expected = [];
	expect(actual).toStrictEqual(expected);
});
it('derives the correct cells for parent with data columns', () => {
	const actual = getSubRows(data, parentRow);
	const expected = getBodyRows(data, dataColumns);
	[0, 1].forEach((rowIdx) => {
		const row = actual[rowIdx];
		expect(row).toBeInstanceOf(DataBodyRow);
		if (!row.isData()) {
			throw new Error('Incorrect instance type');
		}
		expect(row.original).toStrictEqual(expected[rowIdx].original);
		expect(actual[rowIdx].cells.length).toStrictEqual(expected[rowIdx].cells.length);
		actual[rowIdx].cells.forEach((_, colIdx) => {
			const cell = actual[rowIdx].cells[colIdx];
			expect(cell).toBeInstanceOf(DataBodyCell);
			const expectedCell = expected[rowIdx].cells[colIdx];
			if (!(cell.isData() && expectedCell.isData())) {
				throw new Error('Incorrect instance type');
			}
			expect(cell.value).toStrictEqual(expectedCell.value);
		});
	});
});
it('derives the correct cellForId when parent has hidden cells', () => {
	const columnedParentRow = getColumnedBodyRows([parentRow], ['firstName'])[0];
	const actual = getSubRows(data, columnedParentRow);
	const expected = getColumnedBodyRows(getBodyRows(data, dataColumns), ['firstName']);
	[0, 1].forEach((rowIdx) => {
		const row = actual[rowIdx];
		expect(row).toBeInstanceOf(DataBodyRow);
		if (!row.isData()) {
			throw new Error('Incorrect instance type');
		}
		expect(row.original).toStrictEqual(expected[rowIdx].original);
		expect(actual[rowIdx].cells.length).toStrictEqual(expected[rowIdx].cells.length);
		actual[rowIdx].cells.forEach((_, colIdx) => {
			const cell = actual[rowIdx].cells[colIdx];
			expect(cell).toBeInstanceOf(DataBodyCell);
			const expectedCell = expected[rowIdx].cells[colIdx];
			if (!(cell.isData() && expectedCell.isData())) {
				throw new Error('Incorrect instance type');
			}
			expect(cell.value).toStrictEqual(expectedCell.value);
		});
		['firstName', 'lastName', 'progress'].forEach((id) => {
			const cell = actual[rowIdx].cellForId[id];
			expect(cell).toBeInstanceOf(DataBodyCell);
			const expectedCell = expected[rowIdx].cellForId[id];
			if (!(cell.isData() && expectedCell.isData())) {
				throw new Error('Incorrect instance type');
			}
			expect(cell.value).toStrictEqual(expectedCell.value);
		});
	});
});
const checkedLabel = () => 'check';
const expandedLabel = () => 'expanded';
const displayColumns = [
	table.display({
		id: 'checked',
		header: 'Checked',
		cell: checkedLabel
	}),
	table.display({
		id: 'expanded',
		header: 'Expanded',
		cell: expandedLabel
	})
];
const displayParentRow = getBodyRows([parentData], displayColumns)[0];
it('derives the correct cells for parent with columns', () => {
	const actual = getSubRows(data, displayParentRow);
	const expected = getBodyRows(data, displayColumns);
	[0, 1].forEach((rowIdx) => {
		const row = actual[rowIdx];
		expect(row).toBeInstanceOf(DataBodyRow);
		if (!row.isData()) {
			throw new Error('Incorrect instance type');
		}
		expect(row.original).toStrictEqual(expected[rowIdx].original);
		expect(actual[rowIdx].cells.length).toStrictEqual(expected[rowIdx].cells.length);
		actual[rowIdx].cells.forEach((_, colIdx) => {
			const cell = actual[rowIdx].cells[colIdx];
			expect(cell).toBeInstanceOf(DisplayBodyCell);
			const expectedCell = expected[rowIdx].cells[colIdx];
			if (!(cell.isDisplay() && expectedCell.isDisplay())) {
				throw new Error('Incorrect instance type');
			}
			expect(cell.label).toEqual(expectedCell.label);
		});
	});
});
