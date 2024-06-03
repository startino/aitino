import { DataBodyCell } from './bodyCells.js';
import { DataBodyRow } from './bodyRows.js';
import { DataColumn } from './columns.js';
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
const column = new DataColumn({
	header: '',
	accessor: 'firstName'
});
it('renders static label', () => {
	const actual = new DataBodyCell({
		column,
		row,
		value: 'Adam'
	});
	expect(actual.render()).toBe('Adam');
});
const state = {
	columns: []
};
it('renders dynamic label with state', () => {
	const actual = new DataBodyCell({
		column,
		row,
		value: 'Adam',
		label: ({ value }, { columns }) =>
			`${String(value).toLowerCase()} with ${columns.length} columns`
	});
	actual.injectState(state);
	expect(actual.render()).toBe('adam with 0 columns');
});
it('throws if rendering dynamically without state', () => {
	const actual = new DataBodyCell({
		column,
		row,
		value: 'Adam',
		label: ({ value }, { columns }) =>
			`${String(value).toLowerCase()} with ${columns.length} columns`
	});
	expect(() => {
		actual.render();
	}).toThrowError('Missing `state` reference');
});
