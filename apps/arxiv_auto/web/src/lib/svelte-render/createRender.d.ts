import type { ComponentEvents, ComponentProps, SvelteComponent } from 'svelte';
import type { Readable } from 'svelte/store';
export type RenderConfig<TComponent extends SvelteComponent = SvelteComponent> =
	| ComponentRenderConfig<TComponent>
	| string
	| number
	| Readable<string | number>;
export type Constructor<TInstance> = new (...args: any[]) => TInstance;
export declare class ComponentRenderConfig<TComponent extends SvelteComponent = SvelteComponent> {
	component: Constructor<TComponent>;
	props?: ComponentProps<TComponent> | Readable<ComponentProps<TComponent>> | undefined;
	constructor(
		component: Constructor<TComponent>,
		props?: ComponentProps<TComponent> | Readable<ComponentProps<TComponent>> | undefined
	);
	eventHandlers: [keyof ComponentEvents<TComponent>, (ev: Event) => void][];
	on<TEventType extends keyof ComponentEvents<TComponent>>(
		type: TEventType,
		handler: (ev: ComponentEvents<TComponent>[TEventType]) => void
	): this;
	children: RenderConfig[];
	slot(...children: RenderConfig[]): this;
}
export declare function createRender<TComponent extends SvelteComponent<Record<string, never>>>(
	component: Constructor<TComponent>
): ComponentRenderConfig<TComponent>;
export declare function createRender<TComponent extends SvelteComponent>(
	component: Constructor<TComponent>,
	props: ComponentProps<TComponent> | Readable<ComponentProps<TComponent>>
): ComponentRenderConfig<TComponent>;
