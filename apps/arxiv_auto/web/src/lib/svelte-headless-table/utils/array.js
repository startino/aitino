import { getCounter } from './counter.js';
export const getDistinct = (items) => {
	return Array.from(getCounter(items).keys());
};
export const getDuplicates = (items) => {
	return Array.from(getCounter(items).entries())
		.filter(([, count]) => count !== 1)
		.map(([key]) => key);
};
