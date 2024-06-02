import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
export declare const addGridLayout: <Item>() => TablePlugin<
	Item,
	Record<string, never>,
	Record<string, never>,
	NewTablePropSet<never>
>;
