import {
	DataColumn,
	DisplayColumn,
	GroupColumn,
	type Column,
	type DataColumnInitBase,
	type DataColumnInitFnAndId,
	type DataColumnInitIdAndKey,
	type DataColumnInitKey,
	type DisplayColumnInit,
	type GroupColumnInit
} from './columns.js';
import type { AnyPlugins } from './types/TablePlugin.js';
import type { ReadOrWritable } from './utils/store.js';
import { type CreateViewModelOptions, type TableViewModel } from './createViewModel.js';
export declare class Table<Item, Plugins extends AnyPlugins = AnyPlugins> {
	data: ReadOrWritable<Item[]>;
	plugins: Plugins;
	constructor(data: ReadOrWritable<Item[]>, plugins: Plugins);
	createColumns(columns: Column<Item, Plugins>[]): Column<Item, Plugins>[];
	column<Id extends Exclude<keyof Item, symbol>>(
		def: DataColumnInitBase<Item, Plugins, Item[Id]> & DataColumnInitKey<Item, Id>
	): DataColumn<Item, Plugins, `${Id}`, Item[Id]>;
	column<Id extends string, Key extends keyof Item>(
		def: DataColumnInitBase<Item, Plugins, Item[Key]> & DataColumnInitIdAndKey<Item, Id, Key>
	): DataColumn<Item, Plugins, Id, Item[Key]>;
	column<Id extends string, Value>(
		def: DataColumnInitBase<Item, Plugins, Value> & DataColumnInitFnAndId<Item, Id, Value>
	): DataColumn<Item, Plugins, Id, Value>;
	group(def: GroupColumnInit<Item, Plugins>): GroupColumn<Item, Plugins>;
	display(def: DisplayColumnInit<Item, Plugins>): DisplayColumn<Item, Plugins>;
	createViewModel(
		columns: Column<Item, Plugins>[],
		options?: CreateViewModelOptions<Item>
	): TableViewModel<Item, Plugins>;
}
export declare const createTable: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	data: ReadOrWritable<Item[]>,
	plugins?: Plugins
) => Table<Item, Plugins>;
