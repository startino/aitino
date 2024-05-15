export const agents = [
	{
		type: 'userproxy',
		description: 'A user proxy agent that executes code.',
		config: {
			name: 'userproxy',
			human_input_mode: 'NEVER',
			max_consecutive_auto_reply: 5,
			system_message: '',
			llm_config: false,
			code_execution_config: {
				work_dir: null,
				use_docker: false
			}
		}
	},
	{
		type: 'assistant',
		description: 'A primary assistant agent that writes plans and code to solve tasks.',
		config: {
			name: 'primary_assistant',
			llm_config: {
				config_list: [
					{
						model: 'gpt-4-1106-preview'
					}
				],
				temperature: 0.1,
				timeout: 600,
				cache_seed: null
			},
			human_input_mode: 'NEVER',
			max_consecutive_auto_reply: 8,
			system_message:
				"You are a helpful assistant that can use available functions when needed to solve problems. At each point, do your best to determine if the user's request has been addressed. IF THE REQUEST HAS NOT BEEN ADDRESSED, RESPOND WITH CODE TO ADDRESS IT. IF A FAILURE OCCURRED (e.g., due to a missing library) AND SOME ADDITIONAL CODE WAS WRITTEN (e.g. code to install the library), ENSURE THAT THE ORIGINAL CODE TO ADDRESS THE TASK STILL GETS EXECUTED. If the request HAS been addressed, respond with a summary of the result. The summary must be written as a coherent helpful response to the user request e.g. 'Sure, here is result to your request ' or 'The tallest mountain in Africa is ..' etc. The summary MUST end with the word TERMINATE. If the  user request is pleasantry or greeting, you should respond with a pleasantry or greeting and TERMINATE."
		}
	}
];
