import { derived } from 'svelte/store';
import { TableComponent } from './tableComponent.js';
export class BodyCell extends TableComponent {
	row;
	constructor({ id, row }) {
		super({ id });
		this.row = row;
	}
	attrs() {
		return derived(super.attrs(), ($baseAttrs) => {
			return {
				...$baseAttrs,
				role: 'cell'
			};
		});
	}
	rowColId() {
		return `${this.row.id}:${this.column.id}`;
	}
	dataRowColId() {
		if (!this.row.isData()) {
			return undefined;
		}
		return `${this.row.dataId}:${this.column.id}`;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isData() {
		return '__data' in this;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isDisplay() {
		return '__display' in this;
	}
}
export class DataBodyCell extends BodyCell {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__data = true;
	column;
	label;
	value;
	constructor({ row, column, label, value }) {
		super({ id: column.id, row });
		this.column = column;
		this.label = label;
		this.value = value;
	}
	render() {
		if (this.label === undefined) {
			return `${this.value}`;
		}
		if (this.state === undefined) {
			throw new Error('Missing `state` reference');
		}
		return this.label(this, this.state);
	}
	clone() {
		const clonedCell = new DataBodyCell({
			row: this.row,
			column: this.column,
			label: this.label,
			value: this.value
		});
		return clonedCell;
	}
}
export class DisplayBodyCell extends BodyCell {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__display = true;
	column;
	label;
	constructor({ row, column, label }) {
		super({ id: column.id, row });
		this.column = column;
		this.label = label;
	}
	render() {
		if (this.state === undefined) {
			throw new Error('Missing `state` reference');
		}
		return this.label(this, this.state);
	}
	clone() {
		const clonedCell = new DisplayBodyCell({
			row: this.row,
			column: this.column,
			label: this.label
		});
		return clonedCell;
	}
}
