import { DataColumn } from './columns.js';
it('prioritizes a provided id', () => {
	const actual = new DataColumn({
		header: 'First Name',
		accessor: 'firstName',
		id: 'name'
	});
	expect(actual.id).toBe('name');
});
it('falls back on the string accessor as id', () => {
	const actual = new DataColumn({
		header: 'First Name',
		accessor: 'firstName'
	});
	expect(actual.id).toBe('firstName');
});
it('throws if id is undefined without string accessor or header', () => {
	expect(() => {
		new DataColumn({
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			accessor: (u) => u.firstName
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
		});
	}).toThrowError('A column id, string accessor, or header is required');
});
