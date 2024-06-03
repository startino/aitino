import { get } from 'svelte/store';
import { recordSetStore } from './store.js';
it('initializes correctly', () => {
	const actual = recordSetStore();
	const expected = {};
	expect(get(actual)).toStrictEqual(expected);
});
it('initializes with values correctly', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	const expected = {
		1: true,
		2: true,
		3: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles an existing value to remove it', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.toggle(1);
	const expected = {
		2: true,
		3: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles the last value to remove it', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.toggle(3);
	const expected = {
		1: true,
		2: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('toggles a non-existing value to add it', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.toggle(4);
	const expected = {
		1: true,
		2: true,
		3: true,
		4: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('adds a value', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.add(4);
	const expected = {
		1: true,
		2: true,
		3: true,
		4: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('adds an existing value and changes nothing', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.add(3);
	const expected = {
		1: true,
		2: true,
		3: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('removes a value', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.remove(3);
	const expected = {
		1: true,
		2: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('removes a non-existing value and changes nothing', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.remove(4);
	const expected = {
		1: true,
		2: true,
		3: true
	};
	expect(get(actual)).toStrictEqual(expected);
});
it('resets the set', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.clear();
	const expected = {};
	expect(get(actual)).toStrictEqual(expected);
});
it('removes false values on init', () => {
	const actual = recordSetStore({
		1: false,
		2: true,
		3: true
	});
	const expected = { 2: true, 3: true };
	expect(get(actual)).toStrictEqual(expected);
});
it('removes false values on update', () => {
	const actual = recordSetStore({
		1: true,
		2: true,
		3: true
	});
	actual.update(($set) => ({ ...$set, 1: false }));
	const expected = { 2: true, 3: true };
	expect(get(actual)).toStrictEqual(expected);
});
