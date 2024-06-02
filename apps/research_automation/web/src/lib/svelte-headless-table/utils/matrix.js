export const getNullMatrix = (width, height) => {
	const result = [];
	// Use a loop to create a new array instance per row.
	for (let i = 0; i < height; i++) {
		result.push(Array(width).fill(null));
	}
	return result;
};
export const getTransposed = (matrix) => {
	const height = matrix.length;
	if (height === 0) {
		return matrix;
	}
	const width = matrix[0].length;
	const result = getNullMatrix(height, width);
	for (let i = 0; i < width; i++) {
		for (let j = 0; j < height; j++) {
			result[i][j] = matrix[j][i];
		}
	}
	// We guarantee that all elements are filled.
	return result;
};
