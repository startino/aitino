import { SvelteComponent } from 'svelte';
import type { ComponentRenderConfig } from './createRender.js';
declare class __sveltets_Render<TComponent extends SvelteComponent> {
	props(): {
		config: ComponentRenderConfig<TComponent>;
	};
	events(): {} & {
		[evt: string]: CustomEvent<any>;
	};
	slots(): {};
}
export type ComponentRendererProps<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['props']
>;
export type ComponentRendererEvents<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['events']
>;
export type ComponentRendererSlots<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['slots']
>;
export default class ComponentRenderer<TComponent extends SvelteComponent> extends SvelteComponent<
	ComponentRendererProps<TComponent>,
	ComponentRendererEvents<TComponent>,
	ComponentRendererSlots<TComponent>
> {}
export {};
