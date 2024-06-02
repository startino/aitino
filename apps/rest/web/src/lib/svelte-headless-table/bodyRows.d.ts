/// <reference types="svelte" />
import { type Readable } from 'svelte/store';
import { BodyCell } from './bodyCells.js';
import type { FlatColumn } from './columns.js';
import { TableComponent } from './tableComponent.js';
import type { AnyPlugins } from './types/TablePlugin.js';
export type BodyRowInit<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	id: string;
	cells: BodyCell<Item, Plugins>[];
	cellForId: Record<string, BodyCell<Item, Plugins>>;
	depth?: number;
	parentRow?: BodyRow<Item, Plugins>;
};
export type BodyRowAttributes<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	role: 'row';
};
export declare abstract class BodyRow<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends TableComponent<Item, Plugins, 'tbody.tr'> {
	cells: BodyCell<Item, Plugins>[];
	/**
	 * Get the cell with a given column id.
	 *
	 * **This includes hidden cells.**
	 */
	cellForId: Record<string, BodyCell<Item, Plugins>>;
	depth: number;
	parentRow?: BodyRow<Item, Plugins>;
	subRows?: BodyRow<Item, Plugins>[];
	constructor({ id, cells, cellForId, depth, parentRow }: BodyRowInit<Item, Plugins>);
	attrs(): Readable<BodyRowAttributes<Item, Plugins>>;
	abstract clone(props?: BodyRowCloneProps): BodyRow<Item, Plugins>;
	isData(): this is DataBodyRow<Item, Plugins>;
	isDisplay(): this is DisplayBodyRow<Item, Plugins>;
}
type BodyRowCloneProps = {
	includeCells?: boolean;
	includeSubRows?: boolean;
};
export type DataBodyRowInit<Item, Plugins extends AnyPlugins = AnyPlugins> = BodyRowInit<
	Item,
	Plugins
> & {
	dataId: string;
	original: Item;
};
export declare class DataBodyRow<Item, Plugins extends AnyPlugins = AnyPlugins> extends BodyRow<
	Item,
	Plugins
> {
	__data: boolean;
	dataId: string;
	original: Item;
	constructor({
		id,
		dataId,
		original,
		cells,
		cellForId,
		depth,
		parentRow
	}: DataBodyRowInit<Item, Plugins>);
	clone({ includeCells, includeSubRows }?: BodyRowCloneProps): DataBodyRow<Item, Plugins>;
}
export type DisplayBodyRowInit<Item, Plugins extends AnyPlugins = AnyPlugins> = BodyRowInit<
	Item,
	Plugins
>;
export declare class DisplayBodyRow<Item, Plugins extends AnyPlugins = AnyPlugins> extends BodyRow<
	Item,
	Plugins
> {
	__display: boolean;
	constructor({ id, cells, cellForId, depth, parentRow }: DisplayBodyRowInit<Item, Plugins>);
	clone({ includeCells, includeSubRows }?: BodyRowCloneProps): DisplayBodyRow<Item, Plugins>;
}
export interface BodyRowsOptions<Item> {
	rowDataId?: (item: Item, index: number) => string;
}
/**
 * Converts an array of items into an array of table `BodyRow`s based on the column structure.
 * @param data The data to display.
 * @param flatColumns The column structure.
 * @returns An array of `BodyRow`s representing the table structure.
 */
export declare const getBodyRows: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	data: Item[],
	flatColumns: FlatColumn<Item, Plugins, any>[],
	{ rowDataId }?: BodyRowsOptions<Item>
) => BodyRow<Item, Plugins>[];
/**
 * Arranges and hides columns in an array of `BodyRow`s based on
 * `columnIdOrder` by transforming the `cells` property of each row.
 *
 * `cellForId` should remain unaffected.
 *
 * @param rows The rows to transform.
 * @param columnIdOrder The column order to transform to.
 * @returns A new array of `BodyRow`s with corrected row references.
 */
export declare const getColumnedBodyRows: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	rows: BodyRow<Item, Plugins>[],
	columnIdOrder: string[]
) => BodyRow<Item, Plugins>[];
/**
 * Converts an array of items into an array of table `BodyRow`s based on a parent row.
 * @param subItems The sub data to display.
 * @param parentRow The parent row.
 * @returns An array of `BodyRow`s representing the child rows of `parentRow`.
 */
export declare const getSubRows: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	subItems: Item[],
	parentRow: BodyRow<Item, Plugins>,
	{ rowDataId }?: BodyRowsOptions<Item>
) => BodyRow<Item, Plugins>[];
export {};
