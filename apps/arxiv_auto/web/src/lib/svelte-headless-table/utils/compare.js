export const compare = (a, b) => {
	if (Array.isArray(a) && Array.isArray(b)) {
		return compareArray(a, b);
	}
	if (typeof a === 'number' && typeof b === 'number') return a - b;
	return a < b ? -1 : a > b ? 1 : 0;
};
export const compareArray = (a, b) => {
	const minLength = Math.min(a.length, b.length);
	for (let i = 0; i < minLength; i++) {
		const order = compare(a[i], b[i]);
		if (order !== 0) return order;
	}
	return 0;
};
