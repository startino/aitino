import { type ClassValue, clsx } from 'clsx';
import type { Node } from '@xyflow/svelte';
import { twMerge } from 'tailwind-merge';
import { cubicOut } from 'svelte/easing';
import type { RequestEvent } from '@sveltejs/kit';
import type { TransitionConfig } from 'svelte/transition';
import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import api, { type schemas } from './api';
import { toast } from 'svelte-sonner';

dayjs.extend(relativeTime);

export const saveCrew = async (crew: schemas['Crew']) => {
	const response = await api
		.PATCH('/crews/{id}', {
			params: {
				path: {
					id: crew.id
				}
			},
			body: {
				receiver_id: crew.receiver_id,
				prompt: crew.prompt,
				profile_id: crew.profile_id,
				title: crew.title,
				published: crew.published,
				description: crew.description,
				agents: crew.agents
			}
		})
		.then(({ data: d, error: e }) => {
			if (e) {
				console.error(`Error saving crew: ${e.detail}`);
				toast.error(`Failed to save crew! Please report to dev team with logs from the console.`);
				return null;
			}
			if (!d) {
				console.error(`No data returned from crew creation`);
				toast.error(`Failed to save crew! Please report to dev team with logs from the console.`);
				return null;
			}
			toast.success('Crew saved.');
			return d;
		})
		.catch((e) => {
			console.error(`Error saving crew: ${e}`);
			toast.error(`Failed to save crew! Please report to dev team with logs from the console.`);
			return null;
		});

	return response ? true : false;
};

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

// creates an array of writable nodes
export function getWritablePrompt(nodes: Node[]): Node[] {
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
