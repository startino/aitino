export declare const nonNull: <T>(value: T | null) => value is T;
export declare const nonUndefined: <T>(value: T | undefined) => value is T;
export declare const nonNullish: <T>(value: T | null | undefined) => value is T;
export declare const isNumber: (value: unknown) => value is number;
