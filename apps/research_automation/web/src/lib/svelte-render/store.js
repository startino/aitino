import { readable } from 'svelte/store';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isReadable = (value) => {
	return value?.subscribe instanceof Function;
};
export const Undefined = readable(undefined);
