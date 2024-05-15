export const crews = [
	{
		prompts: [
			{
				title: 'this is a label for the input',
				content: "this is the input's content. will usually be a task"
			}
		],
		receiver: {
			id: '0'
		},
		groups: [
			{
				receiver: 1,
				agents: [
					{
						id: '1'
					},
					{
						id: '2'
					}
				]
			},
			{
				receiver: 3,
				agents: [
					{
						id: '3'
					},
					{
						id: '4'
					}
				]
			}
		]
	}
];
