import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
export type ValidChildrenKey<Item> = {
	[Key in keyof Item]: Item[Key] extends Item[] ? Key : never;
}[keyof Item];
export type ValidChildrenFn<Item> = (item: Item) => Item[] | undefined;
export interface SubRowsConfig<Item> {
	children: ValidChildrenKey<Item> | ValidChildrenFn<Item>;
}
export declare const addSubRows: <Item>({
	children
}: SubRowsConfig<Item>) => TablePlugin<
	Item,
	Record<string, never>,
	Record<string, never>,
	NewTablePropSet<never>
>;
