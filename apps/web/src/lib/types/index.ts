import type { Variant } from '$lib/components/ui/button';

export type SvelteEvent<E extends Event = Event, T extends EventTarget = Element> = E & {
	currentTarget: EventTarget & T;
};

export type PanelAction = {
	name: string;
	loading?: boolean;
	buttonVariant?: Variant;
	onclick?: (e: Event) => void;
	isCustom?: boolean;
};


export type Categories =
	| 'multi-agents'
	| 'automation'
	| 'tutorial'
	| 'reviews'
	| 'top-softwares'
	| 'ai'
	| 'learning'
	| 'mathematics'
	| 'engineering'
	| 'computer-science'
	| 'economics'
	| 'business'
	| 'art'
	| 'music'
	| 'technology'
	| 'science-fiction';
