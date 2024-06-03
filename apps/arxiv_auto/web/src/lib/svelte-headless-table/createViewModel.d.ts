/// <reference types="svelte" />
import { type Readable, type Writable } from 'svelte/store';
import { BodyRow } from './bodyRows.js';
import { FlatColumn, type Column } from './columns.js';
import type { Table } from './createTable.js';
import { HeaderRow } from './headerRows.js';
import type { AnyPlugins, PluginStates } from './types/TablePlugin.js';
export type TableAttributes<Item, Plugins extends AnyPlugins = AnyPlugins> = Record<
	string,
	unknown
> & {
	role: 'table';
};
export type TableHeadAttributes<Item, Plugins extends AnyPlugins = AnyPlugins> = Record<
	string,
	unknown
>;
export type TableBodyAttributes<Item, Plugins extends AnyPlugins = AnyPlugins> = Record<
	string,
	unknown
> & {
	role: 'rowgroup';
};
export interface TableViewModel<Item, Plugins extends AnyPlugins = AnyPlugins> {
	flatColumns: FlatColumn<Item, Plugins>[];
	tableAttrs: Readable<TableAttributes<Item, Plugins>>;
	tableHeadAttrs: Readable<TableHeadAttributes<Item, Plugins>>;
	tableBodyAttrs: Readable<TableBodyAttributes<Item, Plugins>>;
	visibleColumns: Readable<FlatColumn<Item, Plugins>[]>;
	headerRows: Readable<HeaderRow<Item, Plugins>[]>;
	originalRows: Readable<BodyRow<Item, Plugins>[]>;
	rows: Readable<BodyRow<Item, Plugins>[]>;
	pageRows: Readable<BodyRow<Item, Plugins>[]>;
	pluginStates: PluginStates<Plugins>;
}
export type ReadOrWritable<T> = Readable<T> | Writable<T>;
export interface PluginInitTableState<Item, Plugins extends AnyPlugins = AnyPlugins>
	extends Omit<TableViewModel<Item, Plugins>, 'pluginStates'> {
	data: ReadOrWritable<Item[]>;
	columns: Column<Item, Plugins>[];
}
export interface TableState<Item, Plugins extends AnyPlugins = AnyPlugins>
	extends TableViewModel<Item, Plugins> {
	data: ReadOrWritable<Item[]>;
	columns: Column<Item, Plugins>[];
}
export interface CreateViewModelOptions<Item> {
	rowDataId?: (item: Item, index: number) => string;
}
export declare const createViewModel: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	table: Table<Item, Plugins>,
	columns: Column<Item, Plugins>[],
	{ rowDataId }?: CreateViewModelOptions<Item>
) => TableViewModel<Item, Plugins>;
