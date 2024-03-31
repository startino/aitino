import { type ClassValue, clsx } from 'clsx';
import { get } from 'svelte/store';
import type { Node } from '@xyflow/svelte';
import { twMerge } from 'tailwind-merge';
import { cubicOut } from 'svelte/easing';
import type { RequestEvent } from '@sveltejs/kit';
import type { TransitionConfig } from 'svelte/transition';
import { getContext as getSvelteContext, setContext as setSvelteContext } from 'svelte';
import { writable } from 'svelte/store';
import type { ContextMap, Crew } from '$lib/types';
import { browser } from '$app/environment';
import { AVATARS, SAMPLE_FULL_NAMES } from '$lib/config';
import { supabase } from './supabase';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(relativeTime);

export function getNodesCount(nodes: Node[]) {
	return {
		agents: nodes.filter((n) => n.type === 'agent').length,
		prompts: nodes.filter((n) => n.type === 'prompt').length
	};
}

export const pickRandomName = () => {
	const genders = ['male', 'female'];
	const genderKey = genders[getRandomIndex(genders)];

	const namesArray = SAMPLE_FULL_NAMES[genderKey];
	const name = namesArray[getRandomIndex(namesArray)];

	return { name, gender: genderKey };
};

export const pickRandomAvatar = () => {
	const { name, gender } = pickRandomName();
	let avatarIndex = getRandomIndex(Array.from({ length: 23 }, (_, i) => i));

	if (gender === 'female') avatarIndex += 25;
	const avatarPath = `agent-avatars/${gender}/`;

	const { data } = supabase.storage.from(avatarPath).getPublicUrl(`${avatarIndex}.png`);
	return { name, avatarUrl: data.publicUrl };
};

function getRandomIndex(array: Array<unknown>) {
	const randomArray = new Uint32Array(1);
	crypto.getRandomValues(randomArray);
	return randomArray[0] % array.length;
}

export const authenticateUser = ({ cookies }: RequestEvent) => {
	if (cookies.get('profileId')) return;

	const profileId = 'edb9a148-a8fc-48bd-beb9-4bf5de602b78'; //crypto.randomUUID();

	const expirationDate = new Date();
	expirationDate.setMonth(expirationDate.getMonth() + 1);

	cookies.set('profileId', profileId, {
		path: '/',
		httpOnly: true,
		sameSite: 'strict',
		secure: process.env.NODE_ENV === 'production',
		expires: expirationDate
	});
};

export function getPremadeInputsMap() {
	if (browser) {
		const inputStr = localStorage.getItem('premade-inputs');

		if (inputStr) {
			return JSON.parse(inputStr) as Record<string, string>;
		}
	}

	return null;
}

export function injectPremadeValues(str: string) {
	let result = str;
	const premadeInputsMap = getPremadeInputsMap();

	if (premadeInputsMap) {
		const matches = str.match(/\{\{(\w*?)\}\}/g);

		if (!matches) return result;

		matches.forEach((m) => {
			if (Object.hasOwn(premadeInputsMap, m)) {
				result = result.replace(m, premadeInputsMap[m]);
			}
		});

		return result;
	}
}

// Get Crew from localStorage
export function getLocalCrew() {
	let crewStr: string | null = null;
	if (browser) {
		crewStr = localStorage.getItem('crew');
	}
	if (!crewStr) return null;

	return JSON.parse(crewStr) as Crew;
}

// creates an array of nodes without the stores
export function getCleanNodes(nodes: Node[]): Node[] {
	const agents = nodes.filter((n) => n.type === 'agent');

	const prompts = nodes
		.filter((n) => n.type === 'prompt')
		.map((n) => {
			const { title, content } = n.data;
			return {
				...n,
				data: {
					title: get(title),
					content: get(content)
				}
			};
		});

	return [...prompts, ...agents];
}

// creates an array of writable nodes
export function getWritableNodes(nodes: Node[]): Node[] {
	return [
		...nodes
			.filter((n) => n.type === 'prompt')
			.map((n) => ({
				...n,
				data: { title: writable(n.data.title), content: writable(n.data.content) }
			})),
		...nodes.filter((n) => n.type === 'agent')
	];
}

export function setContext<K extends keyof ContextMap>(key: K, value: ContextMap[K]) {
	return setSvelteContext(key, value);
}

export function getContext<K extends keyof ContextMap>(key: K): ContextMap[K] {
	return getSvelteContext<ContextMap[K]>(key);
}

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

type FlyAndScaleParams = {
	y?: number;
	x?: number;
	start?: number;
	duration?: number;
};

export const flyAndScale = (
	node: Element,
	params: FlyAndScaleParams = { y: -8, x: 0, start: 0.95, duration: 150 }
): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === 'none' ? '' : style.transform;

	const scaleConversion = (valueA: number, scaleA: [number, number], scaleB: [number, number]) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (style: Record<string, number | string | undefined>): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, '');
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};

type DateStyle = Intl.DateTimeFormatOptions['dateStyle'];

export function formatDate(date: string, dateStyle: DateStyle = 'medium', locales = 'en') {
	const formatter = new Intl.DateTimeFormat(locales, { dateStyle });
	return formatter.format(new Date(date));
}

// Uses timezone and time to return the HH:MM format
export function getLocalTime(date: string): string {
	// TODO: use time zone to get user's actual time
	const sessionDate = new Date(date);
	const hour = sessionDate.getHours();
	const minutes = sessionDate.getMinutes();
	return `${hour}:${minutes.toString().padStart(2, '0')}`;
}

export function daysRelativeToToday(date: string): string {
	const now = new Date();
	const then = new Date(date);
	if (now.toDateString() === then.toDateString()) return 'Today';
	if (now.toDateString() === new Date(then.getTime() + 86400000).toDateString()) return 'Yesterday';
	const diff = now.getTime() - then.getTime();
	const daysSince = Math.floor(diff / (1000 * 60 * 60 * 24));
	return daysSince.toString();
}

// Create our number formatter.
const formatter = new Intl.NumberFormat('en-US', {
	style: 'currency',
	currency: 'USD',
	minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
	maximumFractionDigits: 0 // (causes 2500.99 to be printed as $2,501)
});

export function formatCurrency(amount: number) {
	if (amount === 0) return 'Free';
	return formatter.format(amount);
}

export function timeSince(dateIsoString: Date | string | number) {
	return dayjs(dateIsoString).fromNow(true);
}
