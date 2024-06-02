export const stringifyCss = (style) => {
	return Object.entries(style)
		.map(([name, value]) => `${name}:${value}`)
		.join(';');
};
