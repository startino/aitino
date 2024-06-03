import { derived, writable } from 'svelte/store';
const MIN_PAGE_SIZE = 1;
export const createPageStore = ({
	items,
	initialPageSize,
	initialPageIndex,
	serverSide,
	serverItemCount
}) => {
	const pageSize = writable(initialPageSize);
	const updatePageSize = (fn) => {
		pageSize.update(($pageSize) => {
			const newPageSize = fn($pageSize);
			return Math.max(newPageSize, MIN_PAGE_SIZE);
		});
	};
	const setPageSize = (newPageSize) => updatePageSize(() => newPageSize);
	const pageIndex = writable(initialPageIndex);
	function calcPageCountAndLimitIndex([$pageSize, $itemCount]) {
		const $pageCount = Math.ceil($itemCount / $pageSize);
		pageIndex.update(($pageIndex) => {
			if ($pageCount > 0 && $pageIndex >= $pageCount) {
				return $pageCount - 1;
			}
			return $pageIndex;
		});
		return $pageCount;
	}
	let pageCount;
	if (serverSide && serverItemCount != null) {
		pageCount = derived([pageSize, serverItemCount], calcPageCountAndLimitIndex);
	} else {
		const itemCount = derived(items, ($items) => $items.length);
		pageCount = derived([pageSize, itemCount], calcPageCountAndLimitIndex);
	}
	const hasPreviousPage = derived(pageIndex, ($pageIndex) => {
		return $pageIndex > 0;
	});
	const hasNextPage = derived([pageIndex, pageCount], ([$pageIndex, $pageCount]) => {
		return $pageIndex < $pageCount - 1;
	});
	return {
		pageSize: {
			subscribe: pageSize.subscribe,
			update: updatePageSize,
			set: setPageSize
		},
		pageIndex,
		pageCount,
		serverItemCount,
		hasPreviousPage,
		hasNextPage
	};
};
export const addPagination =
	({ initialPageIndex = 0, initialPageSize = 10, serverSide = false, serverItemCount } = {}) =>
	() => {
		const prePaginatedRows = writable([]);
		const paginatedRows = writable([]);
		const { pageSize, pageIndex, pageCount, hasPreviousPage, hasNextPage } = createPageStore({
			items: prePaginatedRows,
			initialPageIndex,
			initialPageSize,
			serverSide,
			serverItemCount
		});
		const pluginState = {
			pageSize,
			pageIndex,
			pageCount,
			hasPreviousPage,
			hasNextPage
		};
		const derivePageRows = (rows) => {
			return derived([rows, pageSize, pageIndex], ([$rows, $pageSize, $pageIndex]) => {
				prePaginatedRows.set($rows);
				if (serverSide) {
					paginatedRows.set($rows);
					return $rows;
				}
				const startIdx = $pageIndex * $pageSize;
				const _paginatedRows = $rows.slice(startIdx, startIdx + $pageSize);
				paginatedRows.set(_paginatedRows);
				return _paginatedRows;
			});
		};
		return {
			pluginState,
			derivePageRows
		};
	};
