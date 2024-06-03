import { stringifyCss } from './css.js';
export const mergeAttributes = (a, b) => {
	if (a.style === undefined && b.style === undefined) {
		return { ...a, ...b };
	}
	return {
		...a,
		...b,
		style: {
			...(typeof a.style === 'object' ? a.style : {}),
			...(typeof b.style === 'object' ? b.style : {})
		}
	};
};
export const finalizeAttributes = (attrs) => {
	if (attrs.style === undefined || typeof attrs.style !== 'object') {
		return attrs;
	}
	return {
		...attrs,
		style: stringifyCss(attrs.style)
	};
};
