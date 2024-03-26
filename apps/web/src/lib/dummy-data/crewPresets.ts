import type { Crew } from '$lib/types';

export const crewPresets: Crew[] = [
	{
		instance_id: 'preset_01',
		composition: {
			receiver: {
				instance_id: '2'
			},
			prompts: [
				{
					id: '1',
					title: 'Prompt 1',
					content: 'Content 1',
					position: {
						x: 0,
						y: 0
					}
				}
			],
			groups: [
				{
					communicator: 'Communicator 1',
					agents: [
						{
							prompt: '1',
							full_name: 'Full Name 1',
							job_title: 'Job Title 1',
							model: 'Model 1',
							unique_id: '1',
							instance_id: '3',
							position: {
								x: 0,
								y: 0
							}
						}
					]
				}
			]
		}
	}
];
