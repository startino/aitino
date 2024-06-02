import { readable, writable } from 'svelte/store';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isReadable = (value) => {
	return value?.subscribe instanceof Function;
};
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isWritable = (store) => {
	return store?.update instanceof Function && store.set instanceof Function;
};
export const Undefined = readable(undefined);
export const UndefinedAs = () => Undefined;
export const arraySetStore = (initial = [], { isEqual = (a, b) => a === b } = {}) => {
	const { subscribe, update, set } = writable(initial);
	const toggle = (item, { clearOthers = false } = {}) => {
		update(($arraySet) => {
			const index = $arraySet.findIndex(($item) => isEqual($item, item));
			if (index === -1) {
				if (clearOthers) {
					return [item];
				}
				return [...$arraySet, item];
			}
			if (clearOthers) {
				return [];
			}
			return [...$arraySet.slice(0, index), ...$arraySet.slice(index + 1)];
		});
	};
	const add = (item) => {
		update(($arraySet) => {
			const index = $arraySet.findIndex(($item) => isEqual($item, item));
			if (index === -1) {
				return [...$arraySet, item];
			}
			return $arraySet;
		});
	};
	const remove = (item) => {
		update(($arraySet) => {
			const index = $arraySet.findIndex(($item) => isEqual($item, item));
			if (index === -1) {
				return $arraySet;
			}
			return [...$arraySet.slice(0, index), ...$arraySet.slice(index + 1)];
		});
	};
	const clear = () => {
		set([]);
	};
	return {
		subscribe,
		update,
		set,
		toggle,
		add,
		remove,
		clear
	};
};
export const recordSetStore = (initial = {}) => {
	const withFalseRemoved = (record) => {
		return Object.fromEntries(Object.entries(record).filter(([, v]) => v));
	};
	const { subscribe, update, set } = writable(withFalseRemoved(initial));
	const updateAndRemoveFalse = (fn) => {
		update(($recordSet) => {
			const newRecordSet = fn($recordSet);
			return withFalseRemoved(newRecordSet);
		});
	};
	const toggle = (item) => {
		update(($recordSet) => {
			if ($recordSet[item] === true) {
				delete $recordSet[item];
				return $recordSet;
			}
			return {
				...$recordSet,
				[item]: true
			};
		});
	};
	const add = (item) => {
		update(($recordSet) => ({
			...$recordSet,
			[item]: true
		}));
	};
	const addAll = (items) => {
		update(($recordSet) => ({
			...$recordSet,
			...Object.fromEntries(items.map((item) => [item, true]))
		}));
	};
	const remove = (item) => {
		update(($recordSet) => {
			delete $recordSet[item];
			return $recordSet;
		});
	};
	const removeAll = (items) => {
		update(($recordSet) => {
			for (const item of items) {
				delete $recordSet[item];
			}
			return $recordSet;
		});
	};
	const clear = () => {
		set({});
	};
	return {
		subscribe,
		update: updateAndRemoveFalse,
		set: (newValue) => updateAndRemoveFalse(() => newValue),
		toggle,
		add,
		addAll,
		remove,
		removeAll,
		clear
	};
};
