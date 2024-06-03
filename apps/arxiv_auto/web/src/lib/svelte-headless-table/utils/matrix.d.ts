import type { Matrix } from '../types/Matrix.js';
export declare const getNullMatrix: (width: number, height: number) => Matrix<null>;
export declare const getTransposed: <T>(matrix: Matrix<T>) => Matrix<T>;
