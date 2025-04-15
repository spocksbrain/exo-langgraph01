# exo Prompt Templates

This directory contains prompt templates for the exo multi-agent system. These templates are used to generate prompts for the various agents in the system.

## Files

- **system_prompt.txt**: System prompt template for the Primary Interface Agent (PIA)
- **user_prompt.txt**: User prompt template for formatting user input and context

## Usage

The prompt templates are used by the exo system to generate prompts for the various agents. They contain placeholders that are replaced with actual values at runtime.

### System Prompt Template

The system prompt template (`system_prompt.txt`) is used to generate the system prompt for the Primary Interface Agent (PIA). It contains placeholders for additional instructions that can be provided at runtime.

Example:
```
You are the Primary Interface Agent (PIA) for the exo multi-agent system...

{additional_instructions}
```

### User Prompt Template

The user prompt template (`user_prompt.txt`) is used to format user input and context for the agents. It contains placeholders for user input, context, conversation history, current time, desktop context, and task history.

Example:
```
User: {user_input}

Context:
{context}

Previous conversation:
{conversation_history}

Current time: {current_time}

Desktop context:
{desktop_context}

Task history:
{task_history}
```

## Customization

You can customize the prompt templates to change the behavior of the agents. For example, you can:

- Add additional instructions to the system prompt
- Change the format of the user prompt
- Add or remove placeholders

When customizing the prompt templates, make sure to keep the placeholders intact, as they are used by the exo system to insert dynamic content.
