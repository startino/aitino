import { derived, readable, writable } from 'svelte/store';
import { BodyRow, getBodyRows, getColumnedBodyRows } from './bodyRows.js';
import { FlatColumn, getFlatColumns } from './columns.js';
import { getHeaderRows, HeaderRow } from './headerRows.js';
import { finalizeAttributes } from './utils/attributes.js';
import { nonUndefined } from './utils/filter.js';
export const createViewModel = (table, columns, { rowDataId } = {}) => {
	const { data, plugins } = table;
	const $flatColumns = getFlatColumns(columns);
	const flatColumns = readable($flatColumns);
	const originalRows = derived([data, flatColumns], ([$data, $flatColumns]) => {
		return getBodyRows($data, $flatColumns, { rowDataId });
	});
	// _stores need to be defined first to pass into plugins for initialization.
	const _visibleColumns = writable([]);
	const _headerRows = writable();
	const _rows = writable([]);
	const _pageRows = writable([]);
	const _tableAttrs = writable({
		role: 'table'
	});
	const _tableHeadAttrs = writable({});
	const _tableBodyAttrs = writable({
		role: 'rowgroup'
	});
	const pluginInitTableState = {
		data,
		columns,
		flatColumns: $flatColumns,
		tableAttrs: _tableAttrs,
		tableHeadAttrs: _tableHeadAttrs,
		tableBodyAttrs: _tableBodyAttrs,
		visibleColumns: _visibleColumns,
		headerRows: _headerRows,
		originalRows,
		rows: _rows,
		pageRows: _pageRows
	};
	const pluginInstances = Object.fromEntries(
		Object.entries(plugins).map(([pluginName, plugin]) => {
			const columnOptions = Object.fromEntries(
				$flatColumns
					.map((c) => {
						const option = c.plugins?.[pluginName];
						if (option === undefined) return undefined;
						return [c.id, option];
					})
					.filter(nonUndefined)
			);
			return [
				pluginName,
				// eslint-disable-next-line @typescript-eslint/no-explicit-any
				plugin({ pluginName, tableState: pluginInitTableState, columnOptions })
			];
		})
	);
	const pluginStates = Object.fromEntries(
		Object.entries(pluginInstances).map(([key, pluginInstance]) => [
			key,
			pluginInstance.pluginState
		])
	);
	const tableState = {
		data,
		columns,
		flatColumns: $flatColumns,
		tableAttrs: _tableAttrs,
		tableHeadAttrs: _tableHeadAttrs,
		tableBodyAttrs: _tableBodyAttrs,
		visibleColumns: _visibleColumns,
		headerRows: _headerRows,
		originalRows,
		rows: _rows,
		pageRows: _pageRows,
		pluginStates
	};
	const deriveTableAttrsFns = Object.values(pluginInstances)
		.map((pluginInstance) => pluginInstance.deriveTableAttrs)
		.filter(nonUndefined);
	let tableAttrs = readable({
		role: 'table'
	});
	deriveTableAttrsFns.forEach((fn) => {
		tableAttrs = fn(tableAttrs);
	});
	const finalizedTableAttrs = derived(tableAttrs, ($tableAttrs) => {
		const $finalizedAttrs = finalizeAttributes($tableAttrs);
		_tableAttrs.set($finalizedAttrs);
		return $finalizedAttrs;
	});
	const deriveTableHeadAttrsFns = Object.values(pluginInstances)
		.map((pluginInstance) => pluginInstance.deriveTableBodyAttrs)
		.filter(nonUndefined);
	let tableHeadAttrs = readable({});
	deriveTableHeadAttrsFns.forEach((fn) => {
		tableHeadAttrs = fn(tableHeadAttrs);
	});
	const finalizedTableHeadAttrs = derived(tableHeadAttrs, ($tableHeadAttrs) => {
		const $finalizedAttrs = finalizeAttributes($tableHeadAttrs);
		_tableHeadAttrs.set($finalizedAttrs);
		return $finalizedAttrs;
	});
	const deriveTableBodyAttrsFns = Object.values(pluginInstances)
		.map((pluginInstance) => pluginInstance.deriveTableBodyAttrs)
		.filter(nonUndefined);
	let tableBodyAttrs = readable({
		role: 'rowgroup'
	});
	deriveTableBodyAttrsFns.forEach((fn) => {
		tableBodyAttrs = fn(tableBodyAttrs);
	});
	const finalizedTableBodyAttrs = derived(tableBodyAttrs, ($tableBodyAttrs) => {
		const $finalizedAttrs = finalizeAttributes($tableBodyAttrs);
		_tableBodyAttrs.set($finalizedAttrs);
		return $finalizedAttrs;
	});
	const deriveFlatColumnsFns = Object.values(pluginInstances)
		.map((pluginInstance) => pluginInstance.deriveFlatColumns)
		.filter(nonUndefined);
	let visibleColumns = flatColumns;
	deriveFlatColumnsFns.forEach((fn) => {
		// Variance of generic type here is unstable. Not sure how to fix.
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		visibleColumns = fn(visibleColumns);
	});
	const injectedColumns = derived(visibleColumns, ($visibleColumns) => {
		_visibleColumns.set($visibleColumns);
		return $visibleColumns;
	});
	const columnedRows = derived(
		[originalRows, injectedColumns],
		([$originalRows, $injectedColumns]) => {
			return getColumnedBodyRows(
				$originalRows,
				$injectedColumns.map((c) => c.id)
			);
		}
	);
	const deriveRowsFns = Object.values(pluginInstances)
		.map((pluginInstance) => pluginInstance.deriveRows)
		.filter(nonUndefined);
	let rows = columnedRows;
	deriveRowsFns.forEach((fn) => {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		rows = fn(rows);
	});
	const injectedRows = derived(rows, ($rows) => {
		// Inject state.
		$rows.forEach((row) => {
			row.injectState(tableState);
			row.cells.forEach((cell) => {
				cell.injectState(tableState);
			});
		});
		// Apply plugin component hooks.
		Object.entries(pluginInstances).forEach(([pluginName, pluginInstance]) => {
			$rows.forEach((row) => {
				if (pluginInstance.hooks?.['tbody.tr'] !== undefined) {
					row.applyHook(pluginName, pluginInstance.hooks['tbody.tr'](row));
				}
				row.cells.forEach((cell) => {
					if (pluginInstance.hooks?.['tbody.tr.td'] !== undefined) {
						cell.applyHook(pluginName, pluginInstance.hooks['tbody.tr.td'](cell));
					}
				});
			});
		});
		_rows.set($rows);
		return $rows;
	});
	const derivePageRowsFns = Object.values(pluginInstances)
		.map((pluginInstance) => pluginInstance.derivePageRows)
		.filter(nonUndefined);
	// Must derive from `injectedRows` instead of `rows` to ensure that `_rows` is set.
	let pageRows = injectedRows;
	derivePageRowsFns.forEach((fn) => {
		// eslint-disable-next-line @typescript-eslint/no-explicit-any
		pageRows = fn(pageRows);
	});
	const injectedPageRows = derived(pageRows, ($pageRows) => {
		// Inject state.
		$pageRows.forEach((row) => {
			row.injectState(tableState);
			row.cells.forEach((cell) => {
				cell.injectState(tableState);
			});
		});
		// Apply plugin component hooks.
		Object.entries(pluginInstances).forEach(([pluginName, pluginInstance]) => {
			$pageRows.forEach((row) => {
				if (pluginInstance.hooks?.['tbody.tr'] !== undefined) {
					row.applyHook(pluginName, pluginInstance.hooks['tbody.tr'](row));
				}
				row.cells.forEach((cell) => {
					if (pluginInstance.hooks?.['tbody.tr.td'] !== undefined) {
						cell.applyHook(pluginName, pluginInstance.hooks['tbody.tr.td'](cell));
					}
				});
			});
		});
		_pageRows.set($pageRows);
		return $pageRows;
	});
	const headerRows = derived(injectedColumns, ($injectedColumns) => {
		const $headerRows = getHeaderRows(
			columns,
			$injectedColumns.map((c) => c.id)
		);
		// Inject state.
		$headerRows.forEach((row) => {
			row.injectState(tableState);
			row.cells.forEach((cell) => {
				cell.injectState(tableState);
			});
		});
		// Apply plugin component hooks.
		Object.entries(pluginInstances).forEach(([pluginName, pluginInstance]) => {
			$headerRows.forEach((row) => {
				if (pluginInstance.hooks?.['thead.tr'] !== undefined) {
					row.applyHook(pluginName, pluginInstance.hooks['thead.tr'](row));
				}
				row.cells.forEach((cell) => {
					if (pluginInstance.hooks?.['thead.tr.th'] !== undefined) {
						cell.applyHook(pluginName, pluginInstance.hooks['thead.tr.th'](cell));
					}
				});
			});
		});
		_headerRows.set($headerRows);
		return $headerRows;
	});
	return {
		tableAttrs: finalizedTableAttrs,
		tableHeadAttrs: finalizedTableHeadAttrs,
		tableBodyAttrs: finalizedTableBodyAttrs,
		visibleColumns: injectedColumns,
		flatColumns: $flatColumns,
		headerRows,
		originalRows,
		rows: injectedRows,
		pageRows: injectedPageRows,
		pluginStates
	};
};
