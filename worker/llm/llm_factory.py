from typing import Any

from langchain_openai import ChatOpenAI

from app.core import get_settings
settings = get_settings()


class LLM_Factory:

    @staticmethod
    async def OpenAI_StructuredOutput(*, input: Any, schema: Any, model: str, temperature: float = 1.0, **kwargs: Any) -> Any:

        llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=model,
            temperature=temperature
        )

        return await llm.with_structured_output(schema=schema).ainvoke(input, **kwargs) # type: ignore