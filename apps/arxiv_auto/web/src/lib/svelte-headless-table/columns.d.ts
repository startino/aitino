import type { DisplayBodyCell } from './bodyCells.js';
import type { TableState } from './createViewModel.js';
import type { DisplayLabel, HeaderLabel } from './types/Label.js';
import type { DataLabel } from './types/Label.js';
import type { AnyPlugins, PluginColumnConfigs } from './types/TablePlugin.js';
export interface ColumnInit<Item, Plugins extends AnyPlugins = AnyPlugins> {
	header: HeaderLabel<Item, Plugins>;
	footer?: HeaderLabel<Item, Plugins>;
	height: number;
	plugins?: PluginColumnConfigs<Plugins>;
}
export declare class Column<Item, Plugins extends AnyPlugins = AnyPlugins> {
	header: HeaderLabel<Item, Plugins>;
	footer?: HeaderLabel<Item, Plugins>;
	height: number;
	plugins?: PluginColumnConfigs<Plugins>;
	constructor({ header, footer, height, plugins }: ColumnInit<Item, Plugins>);
	isFlat(): this is FlatColumn<Item, Plugins>;
	isData(): this is DataColumn<Item, Plugins>;
	isDisplay(): this is DisplayColumn<Item, Plugins>;
	isGroup(): this is GroupColumn<Item, Plugins>;
}
export type FlatColumnInit<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Id extends string = any
> = Omit<ColumnInit<Item, Plugins>, 'height'> & {
	id?: Id;
};
export declare class FlatColumn<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Id extends string = any
> extends Column<Item, Plugins> {
	__flat: boolean;
	id: Id;
	constructor({ header, footer, plugins, id }: FlatColumnInit<Item, Plugins>);
}
export type DataColumnInit<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Id extends string = string,
	Value = unknown
> = DataColumnInitBase<Item, Plugins, Value> &
	(
		| (Id extends keyof Item ? DataColumnInitKey<Item, Id> : never)
		| DataColumnInitIdAndKey<Item, Id, keyof Item>
		| DataColumnInitFnAndId<Item, Id, Value>
	);
export type DataColumnInitBase<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Value = unknown
> = Omit<ColumnInit<Item, Plugins>, 'height'> & {
	cell?: DataLabel<Item, Plugins, Value>;
};
export type DataColumnInitKey<Item, Id extends keyof Item> = {
	accessor: Id;
	id?: Id;
};
export type DataColumnInitIdAndKey<Item, Id extends string, Key extends keyof Item> = {
	accessor: Key;
	id?: Id;
};
export type DataColumnInitFnAndId<Item, Id extends string, Value> = {
	accessor: keyof Item | ((item: Item) => Value);
	id?: Id;
};
export declare class DataColumn<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Id extends string = any,
	Value = any
> extends FlatColumn<Item, Plugins, Id> {
	__data: boolean;
	cell?: DataLabel<Item, Plugins, Value>;
	accessorKey?: keyof Item;
	accessorFn?: (item: Item) => Value;
	constructor({
		header,
		footer,
		plugins,
		cell,
		accessor,
		id
	}: DataColumnInit<Item, Plugins, Id, Value>);
	getValue(item: Item): any;
}
export type DisplayColumnDataGetter<Item, Plugins extends AnyPlugins = AnyPlugins> = (
	cell: DisplayBodyCell<Item>,
	state?: TableState<Item, Plugins>
) => unknown;
export type DisplayColumnInit<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Id extends string = any
> = FlatColumnInit<Item, Plugins, Id> & {
	cell: DisplayLabel<Item, Plugins>;
	data?: DisplayColumnDataGetter<Item, Plugins>;
};
export declare class DisplayColumn<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Id extends string = any
> extends FlatColumn<Item, Plugins, Id> {
	__display: boolean;
	cell: DisplayLabel<Item, Plugins>;
	data?: DisplayColumnDataGetter<Item, Plugins>;
	constructor({ header, footer, plugins, id, cell, data }: DisplayColumnInit<Item, Plugins, Id>);
}
export type GroupColumnInit<Item, Plugins extends AnyPlugins = AnyPlugins> = Omit<
	ColumnInit<Item, Plugins>,
	'height'
> & {
	columns: Column<Item, Plugins>[];
};
export declare class GroupColumn<Item, Plugins extends AnyPlugins = AnyPlugins> extends Column<
	Item,
	Plugins
> {
	__group: boolean;
	columns: Column<Item, Plugins>[];
	ids: string[];
	constructor({ header, footer, columns, plugins }: GroupColumnInit<Item, Plugins>);
}
export declare const getFlatColumnIds: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	columns: Column<Item, Plugins>[]
) => string[];
export declare const getFlatColumns: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	columns: Column<Item, Plugins>[]
) => FlatColumn<Item, Plugins, any>[];
