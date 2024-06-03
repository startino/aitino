/// <reference types="svelte" />
import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type Writable } from 'svelte/store';
export interface ColumnOrderConfig {
	initialColumnIdOrder?: string[];
	hideUnspecifiedColumns?: boolean;
}
export interface ColumnOrderState {
	columnIdOrder: Writable<string[]>;
}
export declare const addColumnOrder: <Item>({
	initialColumnIdOrder,
	hideUnspecifiedColumns
}?: ColumnOrderConfig) => TablePlugin<
	Item,
	ColumnOrderState,
	Record<string, never>,
	NewTablePropSet<never>
>;
