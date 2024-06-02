export interface Clonable<T> {
	clone(): T;
}
export declare const isClonable: <T>(obj: unknown) => obj is Clonable<T>;
/**
 * Create a new instance of a class instance with all properties shallow
 * copied. This is unsafe as it does not re-run the constructor. Therefore,
 * cloned instances will share a reference to the same property instances.
 * @param source The original instance object.
 * @param props Any additional properties to override.
 * @returns A new instance object with all properties shallow copied.
 */
export declare const unsafeClone: <T extends object>(
	source: T,
	props?: Partial<T> | undefined
) => T;
