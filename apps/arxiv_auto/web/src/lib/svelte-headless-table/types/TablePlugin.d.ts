/// <reference types="svelte" />
import type { BodyCell, BodyCellAttributes } from '../bodyCells.js';
import type { BodyRow, BodyRowAttributes } from '../bodyRows.js';
import type { DataColumn, FlatColumn } from '../columns.js';
import type { HeaderCell, HeaderCellAttributes } from '../headerCells.js';
import type { HeaderRow, HeaderRowAttributes } from '../headerRows.js';
import type {
	PluginInitTableState,
	TableAttributes,
	TableBodyAttributes,
	TableHeadAttributes
} from '../createViewModel.js';
import type { Readable } from 'svelte/store';
export type TablePlugin<
	Item,
	PluginState,
	ColumnOptions,
	TablePropSet extends AnyTablePropSet = AnyTablePropSet,
	TableAttributeSet extends AnyTableAttributeSet = AnyTableAttributeSet
> = (
	init: TablePluginInit<Item, ColumnOptions>
) => TablePluginInstance<Item, PluginState, ColumnOptions, TablePropSet, TableAttributeSet>;
export type TablePluginInit<Item, ColumnOptions> = {
	pluginName: string;
	tableState: PluginInitTableState<Item>;
	columnOptions: Record<string, ColumnOptions>;
};
export type TablePluginInstance<
	Item,
	PluginState,
	ColumnOptions,
	TablePropSet extends AnyTablePropSet = AnyTablePropSet,
	TableAttributeSet extends AnyTableAttributeSet = AnyTableAttributeSet
> = {
	pluginState: PluginState;
	transformFlatColumnsFn?: Readable<TransformFlatColumnsFn<Item>>;
	deriveFlatColumns?: DeriveFlatColumnsFn<Item>;
	deriveRows?: DeriveRowsFn<Item>;
	derivePageRows?: DeriveRowsFn<Item>;
	deriveTableAttrs?: DeriveFn<TableAttributes<Item>>;
	deriveTableHeadAttrs?: DeriveFn<TableHeadAttributes<Item>>;
	deriveTableBodyAttrs?: DeriveFn<TableBodyAttributes<Item>>;
	columnOptions?: ColumnOptions;
	hooks?: TableHooks<Item, TablePropSet, TableAttributeSet>;
};
export type AnyPlugins = Record<any, TablePlugin<any, any, any, any, any>>;
export type AnyPluginInstances = Record<any, TablePluginInstance<any, any, any, any, any>>;
export type TransformFlatColumnsFn<Item> = (flatColumns: DataColumn<Item>[]) => DataColumn<Item>[];
export type DeriveFlatColumnsFn<Item> = <Col extends FlatColumn<Item>>(
	flatColumns: Readable<Col[]>
) => Readable<Col[]>;
export type DeriveRowsFn<Item> = <Row extends BodyRow<Item>>(
	rows: Readable<Row[]>
) => Readable<Row[]>;
export type DeriveFn<T> = (obj: Readable<T>) => Readable<T>;
export type Components<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	'thead.tr': HeaderRow<Item, Plugins>;
	'thead.tr.th': HeaderCell<Item, Plugins>;
	'tbody.tr': BodyRow<Item, Plugins>;
	'tbody.tr.td': BodyCell<Item, Plugins>;
};
export type AttributesForKey<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	'thead.tr': HeaderRowAttributes<Item, Plugins>;
	'thead.tr.th': HeaderCellAttributes<Item, Plugins>;
	'tbody.tr': BodyRowAttributes<Item, Plugins>;
	'tbody.tr.td': BodyCellAttributes<Item, Plugins>;
};
export type ComponentKeys = keyof Components<unknown>;
type TablePropSet<
	PropSet extends {
		[K in ComponentKeys]?: unknown;
	}
> = {
	[K in ComponentKeys]: PropSet[K];
};
export type NewTablePropSet<
	PropSet extends {
		[K in ComponentKeys]?: unknown;
	}
> = {
	[K in ComponentKeys]: unknown extends PropSet[K] ? never : PropSet[K];
};
export type AnyTablePropSet = TablePropSet<any>;
type TableAttributeSet<
	AttributeSet extends {
		[K in ComponentKeys]?: unknown;
	}
> = {
	[K in ComponentKeys]: AttributeSet[K];
};
export type NewTableAttributeSet<
	AttributeSet extends {
		[K in ComponentKeys]?: unknown;
	}
> = {
	[K in ComponentKeys]: unknown extends AttributeSet[K] ? never : AttributeSet[K];
};
export type AnyTableAttributeSet = TableAttributeSet<any>;
export type TableHooks<
	Item,
	PropSet extends AnyTablePropSet = AnyTablePropSet,
	AttributeSet extends AnyTableAttributeSet = AnyTableAttributeSet
> = {
	[ComponentKey in keyof Components<Item>]?: (
		component: Components<Item>[ComponentKey]
	) => ElementHook<PropSet[ComponentKey], AttributeSet[ComponentKey]>;
};
export type ElementHook<Props, Attributes> = {
	props?: Readable<Props>;
	attrs?: Readable<Attributes>;
};
export type PluginStates<Plugins extends AnyPlugins> = {
	[K in keyof Plugins]: ReturnType<Plugins[K]>['pluginState'];
};
type TablePropSetForPluginKey<Plugins extends AnyPlugins> = {
	[K in keyof Plugins]: Plugins[K] extends TablePlugin<any, any, any, infer TablePropSet>
		? TablePropSet
		: never;
};
export type PluginTablePropSet<Plugins extends AnyPlugins> = {
	[ComponentKey in ComponentKeys]: {
		[PluginKey in keyof Plugins]: TablePropSetForPluginKey<Plugins>[PluginKey][ComponentKey];
	};
};
export type PluginColumnConfigs<Plugins extends AnyPlugins> = Partial<{
	[K in keyof Plugins]: ReturnType<Plugins[K]>['columnOptions'];
}>;
export {};
