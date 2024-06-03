/// <reference types="svelte" />
import { type Readable } from 'svelte/store';
import type {
	AnyPlugins,
	ComponentKeys,
	ElementHook,
	PluginTablePropSet
} from './types/TablePlugin.js';
import type { TableState } from './createViewModel.js';
import type { Clonable } from './utils/clone.js';
export interface TableComponentInit {
	id: string;
}
export declare abstract class TableComponent<
	Item,
	Plugins extends AnyPlugins,
	Key extends ComponentKeys
> implements Clonable<TableComponent<Item, Plugins, Key>>
{
	id: string;
	constructor({ id }: TableComponentInit);
	private attrsForName;
	attrs(): Readable<Record<string, unknown>>;
	private propsForName;
	props(): Readable<PluginTablePropSet<Plugins>[Key]>;
	state?: TableState<Item, Plugins>;
	injectState(state: TableState<Item, Plugins>): void;
	applyHook(
		pluginName: string,
		hook: ElementHook<Record<string, unknown>, Record<string, unknown>>
	): void;
	abstract clone(): TableComponent<Item, Plugins, Key>;
}
