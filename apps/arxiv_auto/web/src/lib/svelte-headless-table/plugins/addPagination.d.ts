/// <reference types="svelte" />
import type { NewTablePropSet, TablePlugin } from '../types/TablePlugin.js';
import { type Readable, type Updater, type Writable } from 'svelte/store';
export type PaginationConfig = {
	initialPageIndex?: number;
	initialPageSize?: number;
} & (
	| {
			serverSide?: false | undefined;
			serverItemCount?: undefined;
	  }
	| {
			serverSide: true;
			serverItemCount: Readable<number>;
	  }
);
export interface PaginationState {
	pageSize: Writable<number>;
	pageIndex: Writable<number>;
	pageCount: Readable<number>;
	hasPreviousPage: Readable<boolean>;
	hasNextPage: Readable<boolean>;
}
export declare const createPageStore: ({
	items,
	initialPageSize,
	initialPageIndex,
	serverSide,
	serverItemCount
}: PageStoreConfig) => {
	pageSize: {
		subscribe: (
			this: void,
			run: import('svelte/store').Subscriber<number>,
			invalidate?: import('svelte/store').Invalidator<number> | undefined
		) => import('svelte/store').Unsubscriber;
		update: (fn: Updater<number>) => void;
		set: (newPageSize: number) => void;
	};
	pageIndex: Writable<number>;
	pageCount: Readable<number>;
	serverItemCount: Readable<number> | undefined;
	hasPreviousPage: Readable<boolean>;
	hasNextPage: Readable<boolean>;
};
export interface PageStoreConfig {
	items: Readable<unknown[]>;
	initialPageSize?: number;
	initialPageIndex?: number;
	serverSide?: boolean;
	serverItemCount?: Readable<number>;
}
export declare const addPagination: <Item>({
	initialPageIndex,
	initialPageSize,
	serverSide,
	serverItemCount
}?: PaginationConfig) => TablePlugin<
	Item,
	PaginationState,
	Record<string, never>,
	NewTablePropSet<never>
>;
