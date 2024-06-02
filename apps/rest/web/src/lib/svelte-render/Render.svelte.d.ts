import { SvelteComponent } from 'svelte';
import type { RenderConfig } from './createRender.js';
declare class __sveltets_Render<TComponent extends SvelteComponent> {
	props(): {
		of: RenderConfig<TComponent>;
	};
	events(): {} & {
		[evt: string]: CustomEvent<any>;
	};
	slots(): {};
}
export type RenderProps<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['props']
>;
export type RenderEvents<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['events']
>;
export type RenderSlots<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['slots']
>;
export default class Render<TComponent extends SvelteComponent> extends SvelteComponent<
	RenderProps<TComponent>,
	RenderEvents<TComponent>,
	RenderSlots<TComponent>
> {}
export {};
