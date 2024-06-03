export class Column {
	header;
	footer;
	height;
	plugins;
	constructor({ header, footer, height, plugins }) {
		this.header = header;
		this.footer = footer;
		this.height = height;
		this.plugins = plugins;
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
	isDisplay() {
		return '__display' in this;
	}
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	isGroup() {
		return '__group' in this;
	}
}
export class FlatColumn extends Column {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__flat = true;
	id;
	constructor({ header, footer, plugins, id }) {
		super({ header, footer, plugins, height: 1 });
		this.id = id ?? String(header);
	}
}
export class DataColumn extends FlatColumn {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__data = true;
	cell;
	accessorKey;
	accessorFn;
	constructor({ header, footer, plugins, cell, accessor, id }) {
		super({ header, footer, plugins, id: 'Initialization not complete' });
		this.cell = cell;
		if (accessor instanceof Function) {
			this.accessorFn = accessor;
		} else {
			this.accessorKey = accessor;
		}
		if (id === undefined && this.accessorKey === undefined && header === undefined) {
			throw new Error('A column id, string accessor, or header is required');
		}
		const accessorKeyId = typeof this.accessorKey === 'string' ? this.accessorKey : null;
		this.id = id ?? accessorKeyId ?? String(header);
	}
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	getValue(item) {
		if (this.accessorFn !== undefined) {
			return this.accessorFn(item);
		}
		if (this.accessorKey !== undefined) {
			return item[this.accessorKey];
		}
		return undefined;
	}
}
export class DisplayColumn extends FlatColumn {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__display = true;
	cell;
	data;
	constructor({ header, footer, plugins, id, cell, data }) {
		super({ header, footer, plugins, id });
		this.cell = cell;
		this.data = data;
	}
}
export class GroupColumn extends Column {
	// TODO Workaround for https://github.com/vitejs/vite/issues/9528
	__group = true;
	columns;
	ids;
	constructor({ header, footer, columns, plugins }) {
		const height = Math.max(...columns.map((c) => c.height)) + 1;
		super({ header, footer, height, plugins });
		this.columns = columns;
		this.ids = getFlatColumnIds(columns);
	}
}
export const getFlatColumnIds = (columns) =>
	columns.flatMap((c) => (c.isFlat() ? [c.id] : c.isGroup() ? c.ids : []));
export const getFlatColumns = (columns) => {
	return columns.flatMap((c) => (c.isFlat() ? [c] : c.isGroup() ? getFlatColumns(c.columns) : []));
};
