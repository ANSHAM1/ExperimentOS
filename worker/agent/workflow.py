from langgraph.graph import START, END, StateGraph # type: ignore[arg-type]

from .state import ExperimentState

from .nodes import (generation_prompt_node, retry_prompt_node, evaluation_prompt_node, code_generation_node, 
                    code_execution_node, code_evaluation_node, retry_node, execution_router)



builder = StateGraph(ExperimentState)


builder.add_node("gen_prompt", generation_prompt_node) # type: ignore[arg-type]

builder.add_node("retry_prompt", retry_prompt_node) # type: ignore[arg-type]

builder.add_node("eval_prompt", evaluation_prompt_node) # type: ignore[arg-type]

builder.add_node("generator", code_generation_node) # type: ignore[arg-type]

builder.add_node("executor", code_execution_node) # type: ignore[arg-type]

builder.add_node("evaluator", code_evaluation_node) # type: ignore[arg-type]

builder.add_node("retry", retry_node) # type: ignore[arg-type]



builder.add_edge(START, "gen_prompt")

builder.add_edge("gen_prompt", "generator")

builder.add_edge("retry_prompt", "generator")

builder.add_edge("eval_prompt", "evaluator")

builder.add_edge("generator", "executor")

builder.add_edge("executor", "retry")

builder.add_conditional_edges(
    "retry",
    execution_router,
    {
        "retry": "retry_prompt",
        "evaluate": "eval_prompt",
        "terminate": END
    },
)

builder.add_edge("evaluator", END)



AgentGraph = builder.compile() # type: ignore[arg-type]