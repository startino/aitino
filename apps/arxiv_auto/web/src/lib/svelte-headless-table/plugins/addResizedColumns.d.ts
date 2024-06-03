/// <reference types="svelte" />
import type { NewTableAttributeSet, NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type Writable } from 'svelte/store';
export interface AddResizedColumnsConfig {
	onResizeEnd?: (ev: Event) => void;
}
export type ResizedColumnsState = {
	columnWidths: Writable<Record<string, number>>;
};
export type ResizedColumnsColumnOptions = {
	initialWidth?: number;
	minWidth?: number;
	maxWidth?: number;
	disable?: boolean;
};
export type ResizedColumnsPropSet = NewTablePropSet<{
	'thead.tr.th': {
		(node: Element): void;
		drag: (node: Element) => void;
		reset: (node: Element) => void;
		disabled: boolean;
	};
}>;
export type ResizedColumnsAttributeSet = NewTableAttributeSet<{
	'thead.tr.th': {
		style?: {
			width: string;
			'min-width': string;
			'max-width': string;
			'box-sizing': 'border-box';
		};
	};
	'tbody.tr.td': {
		style?: {
			width: string;
			'min-width': string;
			'max-width': string;
			'box-sizing': 'border-box';
		};
	};
}>;
export declare const addResizedColumns: <Item>({
	onResizeEnd
}?: AddResizedColumnsConfig) => TablePlugin<
	Item,
	ResizedColumnsState,
	ResizedColumnsColumnOptions,
	ResizedColumnsPropSet,
	ResizedColumnsAttributeSet
>;
