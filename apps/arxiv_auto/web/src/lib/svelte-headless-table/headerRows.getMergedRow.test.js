import { DataHeaderCell, GroupHeaderCell } from './headerCells.js';
import { getMergedRow } from './headerRows.js';
it('merges two sets of group cells', () => {
	const cells = [
		new GroupHeaderCell({
			label: 'Name',
			colspan: 1,
			colstart: 0,
			allIds: ['firstName', 'lastName'],
			ids: ['firstName']
		}),
		new GroupHeaderCell({
			label: 'Name',
			colspan: 1,
			colstart: 1,
			allIds: ['firstName', 'lastName'],
			ids: ['lastName']
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 2,
			allIds: ['age', 'status'],
			ids: ['age']
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 3,
			allIds: ['age', 'status'],
			ids: ['status']
		})
	];
	const actual = getMergedRow(cells);
	const expected = [
		new GroupHeaderCell({
			label: 'Name',
			colspan: 2,
			colstart: 0,
			allIds: ['firstName', 'lastName'],
			ids: ['firstName', 'lastName']
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 2,
			colstart: 2,
			allIds: ['age', 'status'],
			ids: ['age', 'status']
		})
	];
	expect(actual).toStrictEqual(expected);
});
it('merges adjacent group cells in front', () => {
	const cells = [
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 0,
			allIds: ['age', 'status'],
			ids: ['age']
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 1,
			allIds: ['age', 'status'],
			ids: ['status']
		}),
		new DataHeaderCell({
			colstart: 2,
			label: 'First Name',
			accessorKey: 'firstName',
			id: 'firstName'
		}),
		new DataHeaderCell({
			colstart: 3,
			label: 'Last Name',
			accessorKey: 'lastName',
			id: 'lastName'
		})
	];
	const actual = getMergedRow(cells);
	const expected = [
		new GroupHeaderCell({
			label: 'Info',
			colspan: 2,
			colstart: 0,
			allIds: ['age', 'status'],
			ids: ['age', 'status']
		}),
		new DataHeaderCell({
			colstart: 2,
			label: 'First Name',
			accessorKey: 'firstName',
			id: 'firstName'
		}),
		new DataHeaderCell({
			colstart: 3,
			label: 'Last Name',
			accessorKey: 'lastName',
			id: 'lastName'
		})
	];
	expect(actual).toStrictEqual(expected);
});
it('merges adjacent group cells behind', () => {
	const cells = [
		new DataHeaderCell({
			colstart: 0,
			label: 'First Name',
			accessorKey: 'firstName',
			id: 'firstName'
		}),
		new DataHeaderCell({
			colstart: 1,
			label: 'Last Name',
			accessorKey: 'lastName',
			id: 'lastName'
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 2,
			allIds: ['age', 'status'],
			ids: ['age']
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 3,
			allIds: ['age', 'status'],
			ids: ['status']
		})
	];
	const actual = getMergedRow(cells);
	const expected = [
		new DataHeaderCell({
			colstart: 0,
			label: 'First Name',
			accessorKey: 'firstName',
			id: 'firstName'
		}),
		new DataHeaderCell({
			colstart: 1,
			label: 'Last Name',
			accessorKey: 'lastName',
			id: 'lastName'
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 2,
			colstart: 2,
			allIds: ['age', 'status'],
			ids: ['age', 'status']
		})
	];
	expect(actual).toStrictEqual(expected);
});
it('does not merge disjoint group cells', () => {
	const cells = [
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 0,
			allIds: ['age', 'status'],
			ids: ['age']
		}),
		new DataHeaderCell({
			colstart: 1,
			label: 'First Name',
			accessorKey: 'firstName',
			id: 'firstName'
		}),
		new DataHeaderCell({
			colstart: 2,
			label: 'Last Name',
			accessorKey: 'lastName',
			id: 'lastName'
		}),
		new GroupHeaderCell({
			colstart: 3,
			label: 'Info',
			colspan: 1,
			allIds: ['age', 'status'],
			ids: ['status']
		})
	];
	const actual = getMergedRow(cells);
	const expected = [
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 0,
			allIds: ['age', 'status'],
			ids: ['age']
		}),
		new DataHeaderCell({
			colstart: 1,
			label: 'First Name',
			accessorKey: 'firstName',
			id: 'firstName'
		}),
		new DataHeaderCell({
			colstart: 2,
			label: 'Last Name',
			accessorKey: 'lastName',
			id: 'lastName'
		}),
		new GroupHeaderCell({
			label: 'Info',
			colspan: 1,
			colstart: 3,
			allIds: ['age', 'status'],
			ids: ['status']
		})
	];
	expect(actual).toStrictEqual(expected);
});
