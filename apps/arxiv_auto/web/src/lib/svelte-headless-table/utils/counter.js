export const getCounter = (items) => {
	const result = new Map();
	items.forEach((item) => {
		result.set(item, (result.get(item) ?? 0) + 1);
	});
	return result;
};
