const baseUrl = '/app/subscription';

// Probably better object oriented way to do this, but sometimes fast is better.
export const features = {
	'Rate Limits': `The guaranteed number of sessions available to in each period.`,
	'Max Agents Per Crew': `The maximum number of agents that can be inside a Crew at one time.`,
	'Access to Crew Editor': `The ability to create and edit Crews.`,
	'Access to Agent Editor': `The ability to create and edit Agents`
};

export type Features = {
	'Rate Limits': string;
	'Max Agents Per Crew': string;
	'Access to Crew Editor': boolean;
	'Access to Agent Editor': boolean;
};

// norp = no risk pricing (model)
export type NorpTier = {
	link?: {
		monthly: string;
		yearly: string;
	};
	index: number;
	name: string;
	subtitle: string;
	cost: number;
	features: Features;
	thumbnail: string;
};

export const norpTiers: NorpTier[] = [
	{
		index: 0,
		name: 'Starter',
		subtitle: 'Keep it going.',
		cost: 0,
		features: {
			'Rate Limits': '4 sessions / day',
			'Max Agents Per Crew': '7',
			'Access to Crew Editor': true,
			'Access to Agent Editor': true
		},
		thumbnail: '/artwork/sailboat.png'
	},
	{
		link: {
			monthly: `${baseUrl}/cruising-monthly`,
			yearly: `${baseUrl}/cruising-yearly`
		},
		index: 1,
		name: 'Cruising',
		subtitle: 'Even the playing field.',
		cost: 21,
		features: {
			'Rate Limits': '3 sessions / 3 hours',
			'Max Agents Per Crew': '15',
			'Access to Crew Editor': true,
			'Access to Agent Editor': true
		},
		thumbnail: '/artwork/plane.png'
	},
	{
		link: {
			monthly: `${baseUrl}/professional-monthly`,
			yearly: `${baseUrl}/professional-yearly`
		},
		index: 2,
		name: 'Professional',
		subtitle: 'Make it unfair.',
		cost: 69,
		features: {
			'Rate Limits': '10 sessions / 3 hours',
			'Max Agents Per Crew': '30',
			'Access to Crew Editor': true,
			'Access to Agent Editor': true
		},
		thumbnail: '/artwork/rocket.png'
	}
];

export const promotions: {
	label: string;
	index: number;
	for: string;
	discount: string;
}[] = [
	{ label: 'Monthly', index: 0, for: 'monthly', discount: '' },
	{ label: 'Anually', index: 1, for: 'anually', discount: '2 Months free' }
];
