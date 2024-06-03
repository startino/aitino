/// <reference types="svelte" />
import type { BodyRow } from '../bodyRows.js';
import type { TablePlugin, NewTablePropSet } from '../types/TablePlugin.js';
import { type Readable, type Writable } from 'svelte/store';
export interface TableFilterConfig {
	fn?: TableFilterFn;
	initialFilterValue?: string;
	includeHiddenColumns?: boolean;
	serverSide?: boolean;
}
export interface TableFilterState<Item> {
	filterValue: Writable<string>;
	preFilteredRows: Readable<BodyRow<Item>[]>;
}
export interface TableFilterColumnOptions<Item> {
	exclude?: boolean;
	getFilterValue?: (value: any) => string;
}
export type TableFilterFn = (props: TableFilterFnProps) => boolean;
export type TableFilterFnProps = {
	filterValue: string;
	value: string;
};
export type TableFilterPropSet = NewTablePropSet<{
	'tbody.tr.td': {
		matches: boolean;
	};
}>;
export declare const addTableFilter: <Item>({
	fn,
	initialFilterValue,
	includeHiddenColumns,
	serverSide
}?: TableFilterConfig) => TablePlugin<
	Item,
	TableFilterState<Item>,
	TableFilterColumnOptions<Item>,
	TableFilterPropSet
>;
