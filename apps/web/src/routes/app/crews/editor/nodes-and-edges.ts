import type { Node, Edge } from '@xyflow/svelte';
import { writable } from 'svelte/store';

const position = { x: 0, y: 0 };
const edgeType = 'smoothstep';

export const data = {
	instance_id: '0',
	composition: {
		prompts: [
			{
				id: 'prompt-1',
				title: 'Main Task Prompt',
				content: 'Plan & execute a full social-media marketing campaign.'
			}
		],
		receiver: {
			instance_id: '1'
		},
		groups: [
			{
				communicator: '1',
				agents: [
					{
						unique_id: '0001',
						instance_id: '1',
						full_name: 'Alice Johnson',
						job_title: 'Content Creator',
						model: 'model-a'
					},
					{
						unique_id: '0004',
						instance_id: '4',
						full_name: 'Michael Smith',
						job_title: 'Graphic Designer',
						model: 'model-b'
					},
					{
						unique_id: '0003',
						instance_id: '3',
						full_name: 'Liza Johnson',
						job_title: 'Content Creator',
						model: 'model-c'
					},
					{
						unique_id: '0012',
						instance_id: '12',
						full_name: 'Emily Brown',
						job_title: 'Marketing Analyst',
						model: 'model-c'
					}
				]
			},
			{
				communicator: '3',
				agents: [
					{
						unique_id: '0002',
						instance_id: '2',
						full_name: 'David Wilson',
						job_title: 'Social Media Strategist',
						model: 'model-b'
					},
					{
						unique_id: '0003',
						instance_id: '3',
						full_name: 'Liza Johnson',
						job_title: 'Content Creator',
						model: 'model-c'
					},
					{
						unique_id: '0011',
						instance_id: '11a',
						full_name: 'Sarah Parker',
						job_title: 'Marketing Coordinator',
						model: 'model-a'
					}
				]
			},
			{
				communicator: '4',
				agents: [
					{
						unique_id: '0004',
						instance_id: '4',
						full_name: 'Michael Smith',
						job_title: 'Graphic Designer',
						model: 'model-a'
					},
					{
						unique_id: '0005',
						instance_id: '5',
						full_name: 'Daniel White',
						job_title: 'Video Editor',
						model: 'model-b'
					},
					{
						unique_id: '0011',
						instance_id: '11b',
						full_name: 'Aria Parker',
						job_title: 'Marketing Coordinator',
						model: 'model-c'
					}
				]
			},
			{
				communicator: '12',
				agents: [
					{
						unique_id: '0012',
						instance_id: '12',
						full_name: 'Emily Brown',
						job_title: 'Marketing Analyst',
						model: 'model-a'
					},
					{
						unique_id: '2004',
						instance_id: '24',
						full_name: 'Mark Anderson',
						job_title: 'SEO Specialist',
						model: 'model-b'
					},
					{
						unique_id: '0025',
						instance_id: '25',
						full_name: 'Laura Garcia',
						job_title: 'Social Media Coordinator',
						model: 'model-c'
					}
				]
			}
		]
	}
};

const agentEncounter: Record<string, boolean> = {};

export const initNodes: Node[] = [
	...data.composition.prompts.map((v) => ({
		id: v.id,
		position,
		type: 'prompt',
		data: { title: writable(v.title), content: writable(v.content) }
	})),
	...data.composition.groups
		.map((g) => [
			...g.agents
				.filter((a) => !agentEncounter[a.instance_id])
				.map((a) => {
					agentEncounter[a.instance_id] = true;
					return {
						id: a.instance_id,
						type: 'agent',
						position,
						data: {
							full_name: writable(a.full_name),
							job_title: writable(a.job_title),
							model: writable(a.model),
							unique_id: a.unique_id,
							instance_id: a.instance_id
						}
					};
				})
		])
		.flat()
];

let edgeId = -1;
export const initEdges: Edge[] = [
	...data.composition.prompts.map((p) => {
		edgeId++;
		return {
			id: 'e' + edgeId.toString(),
			source: p.id,
			target: data.composition.receiver.instance_id,
			type: edgeType,
			animated: true
		};
	}),
	...data.composition.groups.reduce((ac: Edge[], g) => {
		const edges: Edge[] = [...ac];

		g.agents.forEach((aSource) => {
			if (aSource.instance_id === g.communicator) {
				edgeId++;
				edges.push(
					...g.agents
						.filter((aTarget) => aSource.instance_id !== aTarget.instance_id)
						.map((aTarget) => {
							edgeId++;
							return {
								id: 'e' + edgeId.toString(),
								source: aSource.instance_id,
								target: aTarget.instance_id,
								type: edgeType,
								animated: true
							};
						})
				);
			}
		});

		return edges;
	}, [])
];
