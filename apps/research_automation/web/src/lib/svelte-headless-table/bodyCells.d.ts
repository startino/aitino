/// <reference types="svelte" />
import { type Readable } from 'svelte/store';
import type { BodyRow } from './bodyRows.js';
import type { DataColumn, DisplayColumn, FlatColumn } from './columns.js';
import { TableComponent } from './tableComponent.js';
import type { DataLabel, DisplayLabel } from './types/Label.js';
import type { AnyPlugins } from './types/TablePlugin.js';
import type { RenderConfig } from 'svelte-render';
export type BodyCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	id: string;
	row: BodyRow<Item, Plugins>;
};
export type BodyCellAttributes<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	role: 'cell';
};
export declare abstract class BodyCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends TableComponent<Item, Plugins, 'tbody.tr.td'> {
	abstract column: FlatColumn<Item, Plugins>;
	row: BodyRow<Item, Plugins>;
	constructor({ id, row }: BodyCellInit<Item, Plugins>);
	abstract render(): RenderConfig;
	attrs(): Readable<BodyCellAttributes<Item, Plugins>>;
	abstract clone(): BodyCell<Item, Plugins>;
	rowColId(): string;
	dataRowColId(): string | undefined;
	isData(): this is DataBodyCell<Item, Plugins>;
	isDisplay(): this is DisplayBodyCell<Item, Plugins>;
}
export type DataBodyCellInit<Item, Plugins extends AnyPlugins = AnyPlugins, Value = unknown> = Omit<
	BodyCellInit<Item, Plugins>,
	'id'
> & {
	column: DataColumn<Item, Plugins>;
	label?: DataLabel<Item, Plugins, Value>;
	value: Value;
};
export type DataBodyCellAttributes<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> = BodyCellAttributes<Item, Plugins>;
export declare class DataBodyCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins,
	Value = unknown
> extends BodyCell<Item, Plugins> {
	__data: boolean;
	column: DataColumn<Item, Plugins>;
	label?: DataLabel<Item, Plugins, Value>;
	value: Value;
	constructor({ row, column, label, value }: DataBodyCellInit<Item, Plugins, Value>);
	render(): RenderConfig;
	clone(): DataBodyCell<Item, Plugins>;
}
export type DisplayBodyCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = Omit<
	BodyCellInit<Item, Plugins>,
	'id'
> & {
	column: DisplayColumn<Item, Plugins>;
	label: DisplayLabel<Item, Plugins>;
};
export declare class DisplayBodyCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends BodyCell<Item, Plugins> {
	__display: boolean;
	column: DisplayColumn<Item, Plugins>;
	label: DisplayLabel<Item, Plugins>;
	constructor({ row, column, label }: DisplayBodyCellInit<Item, Plugins>);
	render(): RenderConfig;
	clone(): DisplayBodyCell<Item, Plugins>;
}
