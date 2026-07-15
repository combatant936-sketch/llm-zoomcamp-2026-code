INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
provider = TracerProvider()
# provider.add_span_processor(
# SimpleSpanProcessor(ConsoleSpanExporter())
# )
from data import SQLiteSpanExporter
provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")   

class RAGBase:

    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model='openai/gpt-oss-120b'
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query, num_results=5):
        return self.index.search(query, num_results=num_results)

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append(doc['filename'])
            lines.append(doc['content'])
            lines.append('')

        return '\n'.join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )

    def llm(self, prompt):
        input_messages = [
            {'role': 'developer', 'content': self.instructions},
            {'role': 'user', 'content': prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )

        return response

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        response = self.llm(prompt)
        return response.output_text
    

class RAGTraced(RAGBase):

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("my_search") as span:
            results = self.index.search(query, num_results=num_results)

            span.set_attribute("my_key", "my_value")
            span.set_attribute("query", query)
            span.set_attribute("num_results", len(results))

            return results

    def llm(self, prompt):
        with tracer.start_as_current_span("my_llm") as span:

            input_messages = [
                {"role": "developer", "content": self.instructions},
                {"role": "user", "content": prompt},
            ]

            response = self.llm_client.responses.create(
                model=self.model,
                input=input_messages,
            )

            span.set_attribute("my_key", "my_value")

            # Now response exists
            if hasattr(response, "usage") and response.usage:
                span.set_attribute(
                    "input_tokens",
                    response.usage.input_tokens,
                )
                span.set_attribute(
                    "output_tokens",
                    response.usage.output_tokens,
                )

            return response

    def rag(self, query):
        with tracer.start_as_current_span("my_rag") as span:

            search_results = self.search(query)
            prompt = self.build_prompt(query, search_results)
            response = self.llm(prompt)

            span.set_attribute("my_key", "my_value")

            return response.output_text