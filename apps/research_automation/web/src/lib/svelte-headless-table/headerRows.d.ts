/// <reference types="svelte" />
import type { Column } from './columns.js';
import { type HeaderCell } from './headerCells.js';
import { TableComponent } from './tableComponent.js';
import type { Matrix } from './types/Matrix.js';
import type { AnyPlugins } from './types/TablePlugin.js';
export type HeaderRowAttributes<Item, Plugins extends AnyPlugins = AnyPlugins> = {
	role: 'row';
};
export interface HeaderRowInit<Item, Plugins extends AnyPlugins = AnyPlugins> {
	id: string;
	cells: HeaderCell<Item, Plugins>[];
}
export declare class HeaderRow<
	Item,
	Plugins extends AnyPlugins = AnyPlugins
> extends TableComponent<Item, Plugins, 'thead.tr'> {
	cells: HeaderCell<Item, Plugins>[];
	constructor({ id, cells }: HeaderRowInit<Item, Plugins>);
	attrs(): import('svelte/store').Readable<{
		role: 'row';
	}>;
	clone(): HeaderRow<Item, Plugins>;
}
export declare const getHeaderRows: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	columns: Column<Item, Plugins>[],
	flatColumnIds?: string[]
) => HeaderRow<Item, Plugins>[];
export declare const getHeaderRowMatrix: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	columns: Column<Item, Plugins>[]
) => Matrix<HeaderCell<Item, Plugins>>;
export declare const getOrderedColumnMatrix: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	columnMatrix: Matrix<HeaderCell<Item, Plugins>>,
	flatColumnIds: string[]
) => Matrix<HeaderCell<Item, Plugins>>;
export declare const headerRowsForRowMatrix: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	rowMatrix: Matrix<HeaderCell<Item, Plugins>>
) => HeaderRow<Item, Plugins>[];
/**
 * Multi-colspan cells will appear as multiple adjacent cells on the same row.
 * Join these adjacent multi-colspan cells and update the colspan property.
 *
 * Non-adjacent multi-colspan cells (due to column ordering) must be cloned
 * from the original .
 *
 * @param cells An array of cells.
 * @returns An array of cells with no duplicate consecutive cells.
 */
export declare const getMergedRow: <Item, Plugins extends AnyPlugins = AnyPlugins>(
	cells: HeaderCell<Item, Plugins>[]
) => HeaderCell<Item, Plugins>[];
