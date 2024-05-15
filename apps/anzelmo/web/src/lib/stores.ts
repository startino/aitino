import { writable, derived } from 'svelte/store';
import type { PhotoType } from './components/photoType';
import { generate_id } from './components/atoms/id';

export interface Cart {
	photos: PhotoType[];
	total: number;
}

// Cart Store stuff
export function createCartStore() {
	const emptyCart: Cart = {
		photos: [],
		total: 0
	};
	const store = writable(emptyCart);
	const { subscribe, set } = store;
	const isBrowser = typeof window !== 'undefined';

	function reset() {
		isBrowser && (localStorage.storable = JSON.stringify(emptyCart));
		set(emptyCart);
		store.update((state) => {
			return emptyCart;
		});
	}

	isBrowser && localStorage.storable && set(JSON.parse(localStorage.storable));

	return {
		subscribe,
		reset,
		set: (storedValue: Cart) => {
			isBrowser && (localStorage.storable = JSON.stringify(storedValue));
			set(storedValue);
		}
	};
}

export let cart = createCartStore();
export function resetCart() {
	cart = createCartStore();
}

// Alert Store stuff
export function createAlertsStore() {
	const _alerts = writable([]);

	function send(message, type = 'addedToCart', timeout) {
		_alerts.update((state) => {
			return [...state, { id: generate_id(), type, message, timeout }];
		});
	}
	const timers = [];
	const alerts = derived(_alerts, ($_alerts, set) => {
		set($_alerts);
		if ($_alerts.length > 0) {
			const timer = setTimeout(() => {
				_alerts.update((state) => {
					state.shift();
					return state;
				});
			}, $_alerts[0].timeout);
			return () => {
				clearTimeout(timer);
			};
		}
	});
	const { subscribe } = alerts;
	return {
		subscribe,
		send,
		addedToCart: (msg, timeout) => send(msg, 'addedToCart', timeout),
		removedFromCart: (msg, timeout) => send(msg, 'removedFromCart', timeout),
		cartEmptied: (msg, timeout) => send(msg, 'cartEmptied', timeout)
	};
}

export const alerts = createAlertsStore();
