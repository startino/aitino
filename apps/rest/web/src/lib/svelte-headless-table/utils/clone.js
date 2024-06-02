export const isClonable = (obj) => {
	return typeof obj.clone === 'function';
};
/**
 * Create a new instance of a class instance with all properties shallow
 * copied. This is unsafe as it does not re-run the constructor. Therefore,
 * cloned instances will share a reference to the same property instances.
 * @param source The original instance object.
 * @param props Any additional properties to override.
 * @returns A new instance object with all properties shallow copied.
 */
export const unsafeClone = (source, props) => {
	const clone = Object.assign(Object.create(Object.getPrototypeOf(source)), source);
	if (props !== undefined) {
		Object.assign(clone, props);
	}
	return clone;
};
