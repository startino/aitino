import { BodyRow } from '../bodyRows.js';
import type { DataLabel } from '../types/Label.js';
import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type ArraySetStore } from '../utils/store.js';
export interface GroupByConfig {
	initialGroupByIds?: string[];
	disableMultiGroup?: boolean;
	isMultiGroupEvent?: (event: Event) => boolean;
}
export interface GroupByState {
	groupByIds: ArraySetStore<string>;
}
export interface GroupByColumnOptions<
	Item,
	Value = any,
	GroupOn extends string | number = any,
	Aggregate = any
> {
	disable?: boolean;
	getAggregateValue?: (values: GroupOn[]) => Aggregate;
	getGroupOn?: (value: Value) => GroupOn;
	cell?: DataLabel<Item>;
}
export type GroupByPropSet = NewTablePropSet<{
	'thead.tr.th': {
		grouped: boolean;
		toggle: (event: Event) => void;
		clear: () => void;
		disabled: boolean;
	};
	'tbody.tr.td': {
		repeated: boolean;
		aggregated: boolean;
		grouped: boolean;
	};
}>;
interface GetGroupedRowsProps {
	repeatCellIds: Record<string, boolean>;
	aggregateCellIds: Record<string, boolean>;
	groupCellIds: Record<string, boolean>;
	allGroupByIds: string[];
}
export declare const getGroupedRows: <
	Item,
	Row extends BodyRow<Item, import('../types/TablePlugin.js').AnyPlugins>,
	GroupOn extends string | number = any
>(
	rows: Row[],
	groupByIds: string[],
	columnOptions: Record<string, GroupByColumnOptions<Item, any, any, any>>,
	{ repeatCellIds, aggregateCellIds, groupCellIds, allGroupByIds }: GetGroupedRowsProps
) => Row[];
export declare const addGroupBy: <Item>({
	initialGroupByIds,
	disableMultiGroup,
	isMultiGroupEvent
}?: GroupByConfig) => TablePlugin<
	Item,
	GroupByState,
	GroupByColumnOptions<Item, any, any, any>,
	GroupByPropSet
>;
export {};
