import { SvelteComponent } from 'svelte';
import type { ComponentProps } from 'svelte';
import type { ComponentRenderConfig } from './createRender.js';
declare class __sveltets_Render<TComponent extends SvelteComponent> {
	props(): {
		instance?: TComponent | undefined;
		config: Omit<ComponentRenderConfig<TComponent>, 'props'>;
		props?: ComponentProps<TComponent> | undefined;
	};
	events(): {} & {
		[evt: string]: CustomEvent<any>;
	};
	slots(): {};
}
export type PropsRendererProps<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['props']
>;
export type PropsRendererEvents<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['events']
>;
export type PropsRendererSlots<TComponent extends SvelteComponent> = ReturnType<
	__sveltets_Render<TComponent>['slots']
>;
export default class PropsRenderer<TComponent extends SvelteComponent> extends SvelteComponent<
	PropsRendererProps<TComponent>,
	PropsRendererEvents<TComponent>,
	PropsRendererSlots<TComponent>
> {}
export {};
