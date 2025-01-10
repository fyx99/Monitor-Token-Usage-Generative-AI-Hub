from gen_ai_hub.orchestration.models.message import SystemMessage, UserMessage
from gen_ai_hub.orchestration.models.template import Template, TemplateValue
from gen_ai_hub.orchestration.models.llm import LLM
from gen_ai_hub.orchestration.models.config import OrchestrationConfig
from gen_ai_hub.orchestration.service import OrchestrationService


def generate_summary(text, model_name):
    """using orchestration service to generate a summary and return usage data"""

    template = Template(
        messages=[
            SystemMessage("You are a helpful summarization assistant."),
            UserMessage(
                "Summarize the following text: {{?text}}"
            ),
        ]
    )

    llm = LLM(name=model_name, version="latest", parameters={"max_tokens": 256, "temperature": 0.2})

    config = OrchestrationConfig(
        template=template,  
        llm=llm,
    )

    orchestration_service = OrchestrationService(api_url="https://api.ai.internalprod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/d9bd1bd1414ecbf5", config=config)


    result = orchestration_service.run(template_values=[
        TemplateValue(name="text", value=text)
    ])
    return result.orchestration_result.choices[0].message.content, result.orchestration_result.usage.prompt_tokens, result.orchestration_result.usage.completion_tokens
