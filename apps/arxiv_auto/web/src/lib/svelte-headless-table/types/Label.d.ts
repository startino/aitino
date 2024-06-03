import type { RenderConfig } from 'svelte-render';
import type { DataBodyCell, DisplayBodyCell } from '../bodyCells.js';
import type { TableState } from '../createViewModel.js';
import type { HeaderCell } from '../headerCells.js';
import type { AnyPlugins } from './TablePlugin.js';
export type DataLabel<Item, Plugins extends AnyPlugins = AnyPlugins, Value = any> = (
	cell: DataBodyCell<Item, AnyPlugins, Value>,
	state: TableState<Item, Plugins>
) => RenderConfig;
export type DisplayLabel<Item, Plugins extends AnyPlugins = AnyPlugins> = (
	cell: DisplayBodyCell<Item>,
	state: TableState<Item, Plugins>
) => RenderConfig;
export type HeaderLabel<Item, Plugins extends AnyPlugins = AnyPlugins> =
	| RenderConfig
	| ((cell: HeaderCell<Item>, state: TableState<Item, Plugins>) => RenderConfig);
