/// <reference types="svelte" />
import { type Readable, type Writable } from 'svelte/store';
export type ReadOrWritable<T> = Readable<T> | Writable<T>;
export declare const isReadable: <T>(value: any) => value is Readable<T>;
export declare const isWritable: <T>(store: any) => store is Writable<T>;
export type WritableKeys<T> = {
	[K in keyof T]: T[K] extends undefined ? Writable<T[K] | undefined> : Writable<T[K]>;
};
export type ReadableKeys<T> = {
	[K in keyof T]: T[K] extends undefined ? Readable<T[K] | undefined> : Readable<T[K]>;
};
export type ReadOrWritableKeys<T> = {
	[K in keyof T]: T[K] extends undefined ? ReadOrWritable<T[K] | undefined> : ReadOrWritable<T[K]>;
};
export declare const Undefined: Readable<undefined>;
export declare const UndefinedAs: <T>() => Readable<T>;
export interface ToggleOptions {
	clearOthers?: boolean;
}
export interface ArraySetStoreOptions<T> {
	isEqual?: (a: T, b: T) => boolean;
}
export interface ArraySetStore<T> extends Writable<T[]> {
	toggle: (item: T, options?: ToggleOptions) => void;
	add: (item: T) => void;
	remove: (item: T) => void;
	clear: () => void;
}
export declare const arraySetStore: <T>(
	initial?: T[],
	{ isEqual }?: ArraySetStoreOptions<T>
) => ArraySetStore<T>;
export interface RecordSetStore<T extends string | number> extends Writable<Record<T, boolean>> {
	toggle: (item: T) => void;
	add: (item: T) => void;
	addAll: (items: T[]) => void;
	remove: (item: T) => void;
	removeAll: (items: T[]) => void;
	clear: () => void;
}
export declare const recordSetStore: <T extends string | number>(
	initial?: Record<T, boolean>
) => RecordSetStore<T>;
