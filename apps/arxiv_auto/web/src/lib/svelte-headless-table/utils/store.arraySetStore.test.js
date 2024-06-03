import { get } from 'svelte/store';
import { arraySetStore } from './store.js';
it('initializes correctly', () => {
	const actual = arraySetStore();
	const expected = [];
	expect(get(actual)).toStrictEqual(expected);
});
it('initializes with values correctly', () => {
	const actual = arraySetStore([1, 2, 3]);
	const expected = [1, 2, 3];
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles an existing value to remove it', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.toggle(1);
	const expected = [2, 3];
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles the last value to remove it', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.toggle(3);
	const expected = [1, 2];
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles a non-existing value to add it', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.toggle(4);
	const expected = [1, 2, 3, 4];
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles an existing value to remove it and clears others', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.toggle(1, { clearOthers: true });
	const expected = [];
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles the last value to remove it', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.toggle(3, { clearOthers: true });
	const expected = [];
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles a non-existing value to add it', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.toggle(4, { clearOthers: true });
	const expected = [4];
	expect(get(actual)).toStrictEqual(expected);
});
it('adds a value', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.add(4);
	const expected = [1, 2, 3, 4];
	expect(get(actual)).toStrictEqual(expected);
});
it('adds an existing value and changes nothing', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.add(3);
	const expected = [1, 2, 3];
	expect(get(actual)).toStrictEqual(expected);
});
it('removes a value', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.remove(3);
	const expected = [1, 2];
	expect(get(actual)).toStrictEqual(expected);
});
it('removes a non-existing value and changes nothing', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.remove(4);
	const expected = [1, 2, 3];
	expect(get(actual)).toStrictEqual(expected);
});
it('resets the set', () => {
	const actual = arraySetStore([1, 2, 3]);
	actual.clear();
	const expected = [];
	expect(get(actual)).toStrictEqual(expected);
});
it('finds the right element with a custom isEqual function', () => {
	const actual = arraySetStore(
		[
			{ id: 0, name: 'Ada' },
			{ id: 1, name: 'Alan' }
		],
		{ isEqual: (a, b) => a.id === b.id }
	);
	actual.add({
		id: 0,
		name: 'Ken'
	});
	const expected = [
		{ id: 0, name: 'Ada' },
		{ id: 1, name: 'Alan' }
	];
	expect(get(actual)).toStrictEqual(expected);
});
