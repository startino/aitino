/// <reference types="svelte" />
import { type Readable } from 'svelte/store';
export declare const isReadable: <T>(value: any) => value is Readable<T>;
export declare const Undefined: Readable<undefined>;
