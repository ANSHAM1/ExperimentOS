from typing import Any

from langchain_openai import ChatOpenAI

from app.core import get_settings
settings = get_settings()


class LLM_Factory:

    @staticmethod
    def OpenRouter_StructuredOutput(*, input: Any, schema: Any, model: str, temperature: float = 1.0, reasoning: bool, **kwargs: Any) -> Any:

        llm = ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_URL,
            model=model,
            temperature=temperature,
            extra_body={
                "reasoning": {
                    "enabled": reasoning,
                }
            }
        )

        return llm.with_structured_output(schema=schema).invoke(input, **kwargs) # type: ignore


    @staticmethod
    def OpenAI_StrucutredOutput(*, input: Any, schema: Any, model: str, temperature: float = 1.0, reasoning: bool, **kwargs: Any) -> Any:

        llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=model,
            temperature=temperature,
            extra_body={
                "reasoning": {
                    "enabled": reasoning,
                }
            }
        )

        return llm.with_structured_output(schema=schema).invoke(input, **kwargs) # type: ignore