export declare const mergeAttributes: <
	T extends Record<string, unknown>,
	U extends Record<string, unknown>
>(
	a: T,
	b: U
) => T & U;
export declare const finalizeAttributes: <T extends Record<string, unknown>>(
	attrs: T
) => Record<string, unknown>;
