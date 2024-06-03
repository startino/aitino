/// <reference types="svelte" />
import type { RenderConfig } from 'svelte-render';
import type { BodyRow } from '../bodyRows.js';
import type { TablePlugin, NewTablePropSet } from '../types/TablePlugin.js';
import { type Readable, type Writable } from 'svelte/store';
import type { PluginInitTableState } from '../createViewModel.js';
export interface ColumnFiltersConfig {
	serverSide?: boolean;
}
export interface ColumnFiltersState<Item> {
	filterValues: Writable<Record<string, unknown>>;
	preFilteredRows: Readable<BodyRow<Item>[]>;
}
export interface ColumnFiltersColumnOptions<Item, FilterValue = any> {
	fn: ColumnFilterFn<FilterValue>;
	initialFilterValue?: FilterValue;
	render?: (props: ColumnRenderConfigPropArgs<Item, FilterValue>) => RenderConfig;
}
interface ColumnRenderConfigPropArgs<Item, FilterValue = any, Value = any>
	extends PluginInitTableState<Item> {
	id: string;
	filterValue: Writable<FilterValue>;
	values: Readable<Value[]>;
	preFilteredRows: Readable<BodyRow<Item>[]>;
	preFilteredValues: Readable<Value[]>;
}
export type ColumnFilterFn<FilterValue = any, Value = any> = (
	props: ColumnFilterFnProps<FilterValue, Value>
) => boolean;
export type ColumnFilterFnProps<FilterValue = any, Value = any> = {
	filterValue: FilterValue;
	value: Value;
};
export type ColumnFiltersPropSet = NewTablePropSet<{
	'thead.tr.th':
		| {
				render?: RenderConfig;
		  }
		| undefined;
}>;
export declare const addColumnFilters: <Item>({
	serverSide
}?: ColumnFiltersConfig) => TablePlugin<
	Item,
	ColumnFiltersState<Item>,
	ColumnFiltersColumnOptions<Item, any>,
	ColumnFiltersPropSet
>;
export declare const matchFilter: ColumnFilterFn<unknown, unknown>;
export declare const textPrefixFilter: ColumnFilterFn<string, string>;
export declare const numberRangeFilter: ColumnFilterFn<[number | null, number | null], number>;
export {};
