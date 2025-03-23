
from langgraph_supervisor import create_supervisor

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from supervisor_assistant.infrastructure.ai.langgraph.agents.micro_business_expert import MicroBusinessExpertAgent
from supervisor_assistant.infrastructure.ai.langgraph.factory.llm_factory import llm_factory

class BusinessAdministratorWorkflow:
    def __init__(self, llm, checkpointer, store):
        self.llm = llm
        if not self.llm:
            self.llm = llm_factory.create_openai_llm()
        self.checkpointer = checkpointer
        if not self.checkpointer:
            self.checkpointer = InMemorySaver()
        self.store = store
        if not self.store:
            self.store = InMemoryStore()
        
        # Create the workflow with supervisor and customer service agent
        self.workflow = create_supervisor(
            agents=[MicroBusinessExpertAgent(self.llm).create_micro_business_expert_agent()],
            model=self.llm,
            prompt="""
            You are Maria Laya, an artificial intelligence assistant on Behalf of Liwaisi Tech.
            
            You must talk directly and concisely due to the customer is talking with you from social media messages. That's why you must be concise in your responses. You always must introduce yourself with a nice salute when the conversations starts. It's important to be friendly and helpful.
            
            Your main role is assist the business operations talking with the customers and solving any issues they may have.
            
            You have access to the following expert for supporting the operation when required:
            
            - Microbusiness Expert: `micro_business_expert` use it for any question about the Liwaisi Tech micro business.
            
            The output language always must be in Colombian Spanish
            
            """,
            supervisor_name="business_administrator",
            output_mode = "last_message"
            
        )
            
def create_new_business_administrator_workflow(
    llm=None,
    checkpointer=None,
    store=None,
    ):
    instance = BusinessAdministratorWorkflow(llm, checkpointer, store)
    return instance.workflow.compile(
        checkpointer=instance.checkpointer,
        store=instance.store
    )
    