from langgraph.graph import START, END, StateGraph # type: ignore

from .state import ExperimentState

from .nodes import (generation_prompt_node, retry_prompt_node, evaluation_prompt_node, code_generation_node, code_execution_node, code_evaluation_node, 
                    increment_retry_node, retry_router)



builder = StateGraph(ExperimentState)


builder.add_node("gen_prompt", generation_prompt_node) # type: ignore

builder.add_node("retry_prompt", retry_prompt_node) # type: ignore

builder.add_node("eval_prompt", evaluation_prompt_node) # type: ignore

builder.add_node("generator", code_generation_node) # type: ignore

builder.add_node("executor", code_execution_node) # type: ignore

builder.add_node("evaluator", code_evaluation_node) # type: ignore

builder.add_node("retry", increment_retry_node) # type: ignore



builder.add_edge(START, "generation_prompt_node")

builder.add_edge("generation_prompt_node", "generator")

builder.add_edge("retry_prompt_node", "generator")

builder.add_edge("evaluation_prompt_node", "evaluator")

builder.add_edge("generator", "executor")

builder.add_conditional_edges(
    "executor",
    retry_router,
    {
        "exe_retry": "executor",
        "retry": "increment_retry_node",
        "evaluate": "evaluation_prompt_node",
        "terminate": END
    },
)

builder.add_edge("increment_retry_node", "retry_prompt_node")

builder.add_edge("evaluator", END)



evaluator_graph = builder.compile() # type: ignore