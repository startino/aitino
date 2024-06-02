import { DisplayBodyCell } from './bodyCells.js';
import { DataBodyRow } from './bodyRows.js';
import { DisplayColumn } from './columns.js';
const user = {
	firstName: 'Adam',
	lastName: 'Smith',
	age: 43,
	visits: 2,
	progress: 50,
	status: 'complicated'
};
const row = new DataBodyRow({
	id: '0',
	dataId: '0',
	original: user,
	cells: [],
	cellForId: {}
});
const column = new DisplayColumn({
	header: '',
	cell: () => '',
	id: 'checked'
});
const state = {};
it('renders dynamic label with state', () => {
	const actual = new DisplayBodyCell({
		column,
		row,
		label: ({ row }) => `row ${row.id} checked`
	});
	actual.injectState(state);
	expect(actual.render()).toBe('row 0 checked');
});
it('throws if rendering dynamically without state', () => {
	const actual = new DisplayBodyCell({
		column,
		row,
		label: ({ row }) => `row ${row.id} checked`
	});
	expect(() => {
		actual.render();
	}).toThrowError('Missing `state` reference');
});
