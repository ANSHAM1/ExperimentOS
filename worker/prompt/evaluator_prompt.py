from langchain_core.prompts import ChatPromptTemplate


code_evaluation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Act as a senior ML/DL engineer reviewing the result of an executed
machine-learning experiment.

Evaluate the execution result against the user's original experiment
request.

Determine the experiment type from the user's request:
- "training": a single model/task
- "comparison": multiple models intended to be compared

Do not invent or recalculate metrics. Use only the values produced by
the executed Python program.

For a training task:
- identify the model
- report its produced metrics/results
- determine whether the requested task was successfully completed

For a comparison task:
- identify every successfully evaluated model
- report their produced metrics
- compare models using the requested metrics
- identify the best model only when the metric direction and results
  support that conclusion
- mention failed models separately

Check for:
- execution failure
- missing results
- missing requested metrics
- model failures
- obvious mismatch between the requested experiment and the produced
  result

Do not assume missing information.
Do not fabricate values.
Do not modify the generated code.
Do not treat stdout as authoritative when structured result data is
available.

Return ONLY the structured output.
""",
        ),
        (
            "human",
            """
Original Experiment Request:

{human_prompt}

Generated Python Code:

{generated_code}

Execution Result:

{execution_result}
""",
        ),
    ]
)