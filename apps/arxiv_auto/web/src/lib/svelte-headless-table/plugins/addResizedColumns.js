import { sum } from '../utils/math.js';
import { keyed } from 'svelte-keyed';
import { derived, writable } from 'svelte/store';
const getDragXPos = (event) => {
	if (event instanceof MouseEvent) return event.clientX;
	if (event instanceof TouchEvent) return event.targetTouches[0].pageX;
	return 0;
};
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const isCellDisabled = (cell, disabledIds) => {
	if (disabledIds.includes(cell.id)) return true;
	if (cell.isGroup() && cell.ids.every((id) => disabledIds.includes(id))) {
		return true;
	}
	return false;
};
export const addResizedColumns =
	({ onResizeEnd } = {}) =>
	({ columnOptions }) => {
		const disabledResizeIds = Object.entries(columnOptions)
			.filter(([, option]) => option.disable === true)
			.map(([columnId]) => columnId);
		const initialWidths = Object.fromEntries(
			Object.entries(columnOptions)
				.filter(([, option]) => option.initialWidth !== undefined)
				.map(([columnId, { initialWidth }]) => [columnId, initialWidth])
		);
		const columnsWidthState = writable({
			current: initialWidths,
			start: {}
		});
		const columnWidths = keyed(columnsWidthState, 'current');
		const pluginState = { columnWidths };
		const dragStartXPosForId = {};
		const nodeForId = {};
		return {
			pluginState,
			hooks: {
				'thead.tr.th': (cell) => {
					const dblClick = (event) => {
						if (isCellDisabled(cell, disabledResizeIds)) return;
						const { target } = event;
						if (target === null) return;
						event.stopPropagation();
						event.preventDefault();
						if (cell.isGroup()) {
							cell.ids.forEach((id) => {
								const node = nodeForId[id];
								if (node !== undefined) {
									columnWidths.update(($columnWidths) => ({
										...$columnWidths,
										[id]: initialWidths[id]
									}));
								}
							});
						} else {
							const node = nodeForId[cell.id];
							if (node !== undefined) {
								columnWidths.update(($columnWidths) => ({
									...$columnWidths,
									[cell.id]: initialWidths[cell.id]
								}));
							}
						}
					};
					let tapedTwice = false;
					const checkDoubleTap = (event) => {
						if (!tapedTwice) {
							tapedTwice = true;
							setTimeout(function () {
								tapedTwice = false;
							}, 300);
							return false;
						}
						event.preventDefault();
						dblClick(event);
					};
					const dragStart = (event) => {
						if (isCellDisabled(cell, disabledResizeIds)) return;
						const { target } = event;
						if (target === null) return;
						event.stopPropagation();
						event.preventDefault();
						dragStartXPosForId[cell.id] = getDragXPos(event);
						columnsWidthState.update(($columnsWidthState) => {
							const $updatedState = {
								...$columnsWidthState,
								start: { ...$columnsWidthState.start }
							};
							if (cell.isGroup()) {
								cell.ids.forEach((id) => {
									$updatedState.start[id] = $columnsWidthState.current[id];
								});
							} else {
								$updatedState.start[cell.id] = $columnsWidthState.current[cell.id];
							}
							return $updatedState;
						});
						if (event instanceof MouseEvent) {
							window.addEventListener('mousemove', dragMove);
							window.addEventListener('mouseup', dragEnd);
						} else {
							window.addEventListener('touchmove', dragMove);
							window.addEventListener('touchend', dragEnd);
						}
					};
					const dragMove = (event) => {
						event.stopPropagation();
						event.preventDefault();
						const deltaWidth = getDragXPos(event) - dragStartXPosForId[cell.id];
						columnsWidthState.update(($columnsWidthState) => {
							const $updatedState = {
								...$columnsWidthState,
								current: { ...$columnsWidthState.current }
							};
							if (cell.isGroup()) {
								const enabledIds = cell.ids.filter((id) => !disabledResizeIds.includes(id));
								const totalStartWidth = sum(enabledIds.map((id) => $columnsWidthState.start[id]));
								enabledIds.forEach((id) => {
									const startWidth = $columnsWidthState.start[id];
									if (startWidth !== undefined) {
										$updatedState.current[id] = Math.max(
											0,
											startWidth + deltaWidth * (startWidth / totalStartWidth)
										);
									}
								});
							} else {
								const startWidth = $columnsWidthState.start[cell.id];
								const { minWidth = 0, maxWidth } = columnOptions[cell.id] ?? {};
								if (startWidth !== undefined) {
									$updatedState.current[cell.id] = Math.min(
										Math.max(minWidth, startWidth + deltaWidth),
										...(maxWidth === undefined ? [] : [maxWidth])
									);
								}
							}
							return $updatedState;
						});
					};
					const dragEnd = (event) => {
						event.stopPropagation();
						event.preventDefault();
						if (cell.isGroup()) {
							cell.ids.forEach((id) => {
								const node = nodeForId[id];
								if (node !== undefined) {
									columnWidths.update(($columnWidths) => ({
										...$columnWidths,
										[id]: node.getBoundingClientRect().width
									}));
								}
							});
						} else {
							const node = nodeForId[cell.id];
							if (node !== undefined) {
								columnWidths.update(($columnWidths) => ({
									...$columnWidths,
									[cell.id]: node.getBoundingClientRect().width
								}));
							}
						}
						onResizeEnd?.(event);
						if (event instanceof MouseEvent) {
							window.removeEventListener('mousemove', dragMove);
							window.removeEventListener('mouseup', dragEnd);
						} else {
							window.removeEventListener('touchmove', dragMove);
							window.removeEventListener('touchend', dragEnd);
						}
					};
					const $props = (node) => {
						nodeForId[cell.id] = node;
						if (cell.isFlat()) {
							columnWidths.update(($columnWidths) => ({
								...$columnWidths,
								[cell.id]: node.getBoundingClientRect().width
							}));
						}
						return {
							destroy() {
								delete nodeForId[cell.id];
							}
						};
					};
					$props.drag = (node) => {
						node.addEventListener('mousedown', dragStart);
						node.addEventListener('touchstart', dragStart);
						return {
							destroy() {
								node.removeEventListener('mousedown', dragStart);
								node.removeEventListener('touchstart', dragStart);
							}
						};
					};
					$props.reset = (node) => {
						node.addEventListener('dblclick', dblClick);
						node.addEventListener('touchend', checkDoubleTap);
						return {
							destroy() {
								node.removeEventListener('dblckick', dblClick);
								node.removeEventListener('touchend', checkDoubleTap);
							}
						};
					};
					$props.disabled = isCellDisabled(cell, disabledResizeIds);
					const props = derived([], () => {
						return $props;
					});
					const attrs = derived(columnWidths, ($columnWidths) => {
						const width = cell.isGroup()
							? sum(cell.ids.map((id) => $columnWidths[id]))
							: $columnWidths[cell.id];
						if (width === undefined) {
							return {};
						}
						const widthPx = `${width}px`;
						return {
							style: {
								width: widthPx,
								'min-width': widthPx,
								'max-width': widthPx,
								'box-sizing': 'border-box'
							}
						};
					});
					return { props, attrs };
				},
				'tbody.tr.td': (cell) => {
					const attrs = derived(columnWidths, ($columnWidths) => {
						const width = $columnWidths[cell.id];
						if (width === undefined) {
							return {};
						}
						const widthPx = `${width}px`;
						return {
							style: {
								width: widthPx,
								'min-width': widthPx,
								'max-width': widthPx,
								'box-sizing': 'border-box'
							}
						};
					});
					return { attrs };
				}
			}
		};
	};
