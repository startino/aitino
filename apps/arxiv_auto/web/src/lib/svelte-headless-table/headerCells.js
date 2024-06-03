import { derived } from 'svelte/store';
import { NBSP } from './constants.js';
import { TableComponent } from './tableComponent.js';
export class HeaderCell extends TableComponent {
	label;
	colspan;
	colstart;
	constructor({ id, label, colspan, colstart }) {
		super({ id });
		this.label = label;
		this.colspan = colspan;
		this.colstart = colstart;
	}
	render() {
		if (this.label instanceof Function) {
			if (this.state === undefined) {
				throw new Error('Missing `state` reference');
			}
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			return this.label(this, this.state);
		}
		return this.label;
	}
	attrs() {
		return derived(super.attrs(), ($baseAttrs) => {
			return {
				...$baseAttrs,
				role: 'columnheader',
				colspan: this.colspan
			};
		});
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isFlat() {
		return '__flat' in this;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isData() {
		return '__data' in this;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isFlatDisplay() {
		return '__flat' in this && '__display' in this;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isGroup() {
		return '__group' in this;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isGroupDisplay() {
		return '__group' in this && '__display' in this;
	}
}
export class FlatHeaderCell extends HeaderCell {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__flat = true;
	constructor({ id, label, colstart }) {
		super({ id, label, colspan: 1, colstart });
	}
	clone() {
		return new FlatHeaderCell({
			id: this.id,
			label: this.label,
			colstart: this.colstart
		});
	}
}
export class DataHeaderCell extends FlatHeaderCell {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__data = true;
	accessorKey;
	accessorFn;
	constructor({ id, label, accessorKey, accessorFn, colstart }) {
		super({ id, label, colstart });
		this.accessorKey = accessorKey;
		this.accessorFn = accessorFn;
	}
	clone() {
		return new DataHeaderCell({
			id: this.id,
			label: this.label,
			accessorFn: this.accessorFn,
			accessorKey: this.accessorKey,
			colstart: this.colstart
		});
	}
}
export class FlatDisplayHeaderCell extends FlatHeaderCell {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__display = true;
	constructor({ id, label = NBSP, colstart }) {
		super({ id, label, colstart });
	}
	clone() {
		return new FlatDisplayHeaderCell({
			id: this.id,
			label: this.label,
			colstart: this.colstart
		});
	}
}
export class GroupHeaderCell extends HeaderCell {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__group = true;
	ids;
	allId;
	allIds;
	constructor({ label, ids, allIds, colspan, colstart }) {
		super({ id: `[${ids.join(',')}]`, label, colspan, colstart });
		this.ids = ids;
		this.allId = `[${allIds.join(',')}]`;
		this.allIds = allIds;
	}
	setIds(ids) {
		this.ids = ids;
		this.id = `[${this.ids.join(',')}]`;
	}
	pushId(id) {
		this.ids = [...this.ids, id];
		this.id = `[${this.ids.join(',')}]`;
	}
	clone() {
		return new GroupHeaderCell({
			label: this.label,
			ids: this.ids,
			allIds: this.allIds,
			colspan: this.colspan,
			colstart: this.colstart
		});
	}
}
export class GroupDisplayHeaderCell extends GroupHeaderCell {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__display = true;
	constructor({ label = NBSP, ids, allIds, colspan = 1, colstart }) {
		super({ label, ids, allIds, colspan, colstart });
	}
	clone() {
		return new GroupDisplayHeaderCell({
			label: this.label,
			ids: this.ids,
			allIds: this.allIds,
			colspan: this.colspan,
			colstart: this.colstart
		});
	}
}
