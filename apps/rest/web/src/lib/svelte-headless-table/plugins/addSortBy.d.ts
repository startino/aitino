/// <reference types="svelte" />
import type { BodyRow } from '../bodyRows.js';
import type { TablePlugin, NewTablePropSet } from '../types/TablePlugin.js';
import { type Readable, type Writable } from 'svelte/store';
export interface SortByConfig {
	initialSortKeys?: SortKey[];
	disableMultiSort?: boolean;
	isMultiSortEvent?: (event: Event) => boolean;
	toggleOrder?: ('asc' | 'desc' | undefined)[];
	serverSide?: boolean;
}
export interface SortByState<Item> {
	sortKeys: WritableSortKeys;
	preSortedRows: Readable<BodyRow<Item>[]>;
}
export interface SortByColumnOptions {
	disable?: boolean;
	getSortValue?: (value: any) => string | number | (string | number)[];
	compareFn?: (left: any, right: any) => number;
	invert?: boolean;
}
export type SortByPropSet = NewTablePropSet<{
	'thead.tr.th': {
		order: 'asc' | 'desc' | undefined;
		toggle: (event: Event) => void;
		clear: () => void;
		disabled: boolean;
	};
	'tbody.tr.td': {
		order: 'asc' | 'desc' | undefined;
	};
}>;
export interface SortKey {
	id: string;
	order: 'asc' | 'desc';
}
export declare const createSortKeysStore: (initKeys: SortKey[]) => WritableSortKeys;
interface ToggleOptions {
	multiSort?: boolean;
	toggleOrder?: ('asc' | 'desc' | undefined)[];
}
export type WritableSortKeys = Writable<SortKey[]> & {
	toggleId: (id: string, options: ToggleOptions) => void;
	clearId: (id: string) => void;
};
export declare const addSortBy: <Item>({
	initialSortKeys,
	disableMultiSort,
	isMultiSortEvent,
	toggleOrder,
	serverSide
}?: SortByConfig) => TablePlugin<Item, SortByState<Item>, SortByColumnOptions, SortByPropSet>;
export {};
