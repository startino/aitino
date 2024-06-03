/// <reference types="svelte" />
import { TableComponent } from './tableComponent.js';
import type { HeaderLabel } from './types/Label.js';
import type { AnyPlugins } from './types/TablePlugin.js';
import type { RenderConfig } from 'svelte-render';
export type HeaderCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	id: string;
	label: HeaderLabel<Item, Plugins>;
	colspan: number;
	colstart: number;
};
export type HeaderCellAttributes<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	role: 'columnheader';
	colspan: number;
};
export declare abstract class HeaderCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends TableComponent<Item, Plugins, 'thead.tr.th'> {
	label: HeaderLabel<Item, Plugins>;
	colspan: number;
	colstart: number;
	constructor({ id, label, colspan, colstart }: HeaderCellInit<Item, Plugins>);
	render(): RenderConfig;
	attrs(): import('svelte/store').Readable<{
		role: 'columnheader';
		colspan: number;
	}>;
	abstract clone(): HeaderCell<Item, Plugins>;
	isFlat(): this is FlatHeaderCell<Item, Plugins>;
	isData(): this is DataHeaderCell<Item, Plugins>;
	isFlatDisplay(): this is FlatDisplayHeaderCell<Item, Plugins>;
	isGroup(): this is GroupHeaderCell<Item, Plugins>;
	isGroupDisplay(): this is GroupDisplayHeaderCell<Item, Plugins>;
}
export type FlatHeaderCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = Omit<
	HeaderCellInit<Item, Plugins>,
	'colspan'
>;
export type FlatHeaderCellAttributes<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> = HeaderCellAttributes<Item, Plugins>;
export declare class FlatHeaderCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends HeaderCell<Item, Plugins> {
	__flat: boolean;
	constructor({ id, label, colstart }: FlatHeaderCellInit<Item, Plugins>);
	clone(): FlatHeaderCell<Item, Plugins>;
}
export type DataHeaderCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = FlatHeaderCellInit<
	Item,
	Plugins
> & {
	accessorKey?: keyof Item;
	accessorFn?: (item: Item) => unknown;
};
export declare class DataHeaderCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends FlatHeaderCell<Item, Plugins> {
	__data: boolean;
	accessorKey?: keyof Item;
	accessorFn?: (item: Item) => unknown;
	constructor({ id, label, accessorKey, accessorFn, colstart }: DataHeaderCellInit<Item, Plugins>);
	clone(): DataHeaderCell<Item, Plugins>;
}
export type FlatDisplayHeaderCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = Omit<
	FlatHeaderCellInit<Item, Plugins>,
	'label'
> & {
	label?: HeaderLabel<Item, Plugins>;
};
export declare class FlatDisplayHeaderCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends FlatHeaderCell<Item, Plugins> {
	__display: boolean;
	constructor({ id, label, colstart }: FlatDisplayHeaderCellInit<Item, Plugins>);
	clone(): FlatDisplayHeaderCell<Item, Plugins>;
}
export type GroupHeaderCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = Omit<
	HeaderCellInit<Item, Plugins>,
	'id'
> & {
	ids: string[];
	allIds: string[];
};
export declare class GroupHeaderCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends HeaderCell<Item, Plugins> {
	__group: boolean;
	ids: string[];
	allId: string;
	allIds: string[];
	constructor({ label, ids, allIds, colspan, colstart }: GroupHeaderCellInit<Item, Plugins>);
	setIds(ids: string[]): void;
	pushId(id: string): void;
	clone(): GroupHeaderCell<Item, Plugins>;
}
export type GroupDisplayHeaderCellInit<Item, Plugins extends AnyPlugins = AnyPlugins> = Omit<
	GroupHeaderCellInit<Item, Plugins>,
	'label' | 'colspan'
> & {
	label?: HeaderLabel<Item, Plugins>;
	colspan?: number;
};
export declare class GroupDisplayHeaderCell<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends GroupHeaderCell<Item, Plugins> {
	__display: boolean;
	constructor({ label, ids, allIds, colspan, colstart }: GroupDisplayHeaderCellInit<Item, Plugins>);
	clone(): GroupDisplayHeaderCell<Item, Plugins>;
}
