from .tools import get_file_path_of_example

fizz_buzz: dict = {
    "id": "00000000-0000-0000-0000-000000000000",
    "profile_id": "6fcde4e6-6592-471b-9d33-dbf7e2ecfab4",
    "title": "FizzBuzz",
    "description": "Makes the crew write a program that prints the numbers from 1 to 100. But for multiples of three print “Fizz” instead of the number and for the multiples of five print “Buzz”. For numbers which are multiples of both three and five print “FizzBuzz”.",
    "receiver_id": "8e26f947-a0e9-4e47-b86f-22930ea948fa",
    "published": False,
    "nodes": [
        "8e26f947-a0e9-4e47-b86f-22930ea948fa",
        "6e541720-b4ac-4c47-abf3-f17147c9a32a",
    ],
    "prompt": {
        "id": "",
        "title": "",
        "content": "Write a program that prints the numbers from 1 to 100. But for multiples of three print “Fizz” instead of the number and for the multiples of five print “Buzz”. For numbers which are multiples of both three and five print “FizzBuzz”.",
    },
    "created_at": "2024-01-01T00:00:00.000Z",
}

markdown_table: dict = {
    "id": "00000000-0000-0000-0000-000000000001",
    "profile_id": "6fcde4e6-6592-471b-9d33-dbf7e2ecfab4",
    "title": "Top 10 LLM Markdown Table",
    "description": "Makes the crew create a markdown table of the 10 best LLMs and comparing their abilities by researching the internet.",
    "receiver_id": "0c0f0b05-e4ff-4d9a-a103-96a9702248f4",
    "published": False,
    "nodes": [
        "8e26f947-a0e9-4e47-b86f-22930ea948fa",
        "0c0f0b05-e4ff-4d9a-a103-96a9702248f4",
    ],
    "prompt": {
        "id": "",
        "title": "",
        "content": "Create a markdown table of the top 10 large language models comparing their abilities by researching on the internet.",
    },
    "created_at": "2024-01-01T00:00:00.000Z",
}

read_file: dict = {
    "id": "00000000-0000-0000-0000-000000000001",
    "profile_id": "6fcde4e6-6592-471b-9d33-dbf7e2ecfab4",
    "title": "Output file content",
    "description": "Read content of file and output it in a nice format",
    "receiver_id": "0c0f0b05-e4ff-4d9a-a103-96a9702248f4",
    "published": False,
    "nodes": [
        "8e26f947-a0e9-4e47-b86f-22930ea948fa",
        # "0c0f0b05-e4ff-4d9a-a103-96a9702248f4",
        "6e541720-b4ac-4c47-abf3-f17147c9a32a",
    ],
    "prompt": {
        "id": "",
        "title": "",
        "content": f"Get the file content of the file '{get_file_path_of_example()}', the 'agent python software' can call what function it has been",
    },
    "created_at": "2024-01-01T00:00:00.000Z",
}
# "6e541720-b4ac-4c47-abf3-f17147c9a32a", agent for code reviewing
# "2ce0b7db-84f7-4d59-8c38-3fcc3fd7da98", agent for writing tables in markdown


move_file: dict = {
    "id": "00000000-0000-0000-0000-000000000001",
    "profile_id": "6fcde4e6-6592-471b-9d33-dbf7e2ecfab4",
    "title": "Output file content",
    "description": "Read content of file and output it in a nice format",
    "receiver_id": "0c0f0b05-e4ff-4d9a-a103-96a9702248f4",
    "published": False,
    "nodes": [
        "8e26f947-a0e9-4e47-b86f-22930ea948fa",
        # "0c0f0b05-e4ff-4d9a-a103-96a9702248f4",
        "6e541720-b4ac-4c47-abf3-f17147c9a32a",
    ],
    "prompt": {
        "id": "",
        "title": "",
        "content": f"Move the file: '{get_file_path_of_example()}' to the destination: {get_file_path_of_example().replace('.txt', '_2.txt')} the 'agent python software' can call what function it has been",
    },
    "created_at": "2024-01-01T00:00:00.000Z",
}

tool, prompt = "alpha vantage tool", "get currency exchange rate between USD and NOK"

test_tool: dict = {
    "id": "00000000-0000-0000-0000-000000000001",
    "profile_id": "070c1d2e-9d72-4854-a55e-52ade5a42071",
    "title": "Test tools",
    "description": "Test the function of the tool and see if it calls and runs properly",
    "receiver_id": "7c707c30-2cfe-46a0-afa7-8bcc38f9687e",
    "published": False,
    "nodes": [
        "7c707c30-2cfe-46a0-afa7-8bcc38f9687e",
    ],
    "prompt": {
        "id": "",
        "title": "",
        "content": f"This is a tool testing environment, use the tool: {tool}, {prompt}. Suggest this function call",
    },
    "created_at": "2024-01-01T00:00:00.000Z",
}
crew_model = test_tool
