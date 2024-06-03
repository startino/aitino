/// <reference types="svelte" />
import type { BodyRow } from '../bodyRows.js';
import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type RecordSetStore } from '../utils/store.js';
import { type Readable, type Writable } from 'svelte/store';
export interface SelectedRowsConfig<Item> {
	initialSelectedDataIds?: Record<string, boolean>;
	linkDataSubRows?: boolean;
}
export interface SelectedRowsState<Item> {
	selectedDataIds: RecordSetStore<string>;
	allRowsSelected: Writable<boolean>;
	someRowsSelected: Readable<boolean>;
	allPageRowsSelected: Writable<boolean>;
	somePageRowsSelected: Readable<boolean>;
	getRowState: (row: BodyRow<Item>) => SelectedRowsRowState;
}
export interface SelectedRowsRowState {
	isSelected: Writable<boolean>;
	isSomeSubRowsSelected: Readable<boolean>;
	isAllSubRowsSelected: Readable<boolean>;
}
export type SelectedRowsPropSet = NewTablePropSet<{
	'tbody.tr': {
		selected: boolean;
		someSubRowsSelected: boolean;
		allSubRowsSelected: boolean;
	};
}>;
export declare const addSelectedRows: <Item>({
	initialSelectedDataIds,
	linkDataSubRows
}?: SelectedRowsConfig<Item>) => TablePlugin<
	Item,
	SelectedRowsState<Item>,
	Record<string, never>,
	SelectedRowsPropSet
>;
