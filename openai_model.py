import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.vectorstores import Chroma
from langchain import PromptTemplate, LLMChain

from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

class Model():
    
    def __init__(self):
        self.llm = OpenAI(temperature=0.2, verbose=True)
        self.embeddings = OpenAIEmbeddings()
        self.resource_agent_executor = None
        self.example_agent_executor = None
        self.resume_agent_executor = None


    async def _get_resume_vs(self, resume_path):
        # read the pdf
        loader = UnstructuredPDFLoader(resume_path)
        # split the document up into array of pages
        pages = loader.load_and_split()
        # create Chroma vector storage
        store = Chroma.from_documents(pages, self.embeddings, collection_name='personal_resume')
        resume_vector_info = VectorStoreInfo(
            name="personal_resume",
            description="A resume that needs to be critiqued, reworded, and improved",
            vectorstore=store
            )

        return resume_vector_info
    
    async def _get_resource_vs(self, resources_path):
        # read the pdf
        loader = UnstructuredPDFLoader(resources_path)
        # split the document up into array of pages
        pages = loader.load_and_split()
        # create Chroma vector storage
        store = Chroma.from_documents(pages, self.embeddings, collection_name='resume_resources')
        resource_vector_info = VectorStoreInfo(
            name="resources",
            description="A collection of tutorials about writing good software engineering resumes",
            vectorstore=store
            )

        return resource_vector_info
    
    async def _get_example_vs(self, example_path):
        # read the pdf
        loader = UnstructuredPDFLoader(example_path)
        # split the document up into array of pages
        pages = loader.load_and_split()
        # create Chroma vector storage
        store = Chroma.from_documents(pages, self.embeddings, collection_name='resume_example')
        example_vector_info = VectorStoreInfo(
            name="example_resume",
            description="Several example resumes to be used as reference",
            vectorstore=store
            )

        return example_vector_info
    
    async def create_router_agent(self):
        resume_path = os.path.join('./resumes', os.listdir('./resumes')[0])
        examples_path = './resources/examples.pdf'
        tutorials_path = './resources/tutorials.pdf'
        
        resource_vector_info = await self._get_resource_vs(tutorials_path)
        example_vector_info = await self._get_example_vs(examples_path)
        resume_vector_info = await self._get_resume_vs(resume_path)

        resource_toolkit = VectorStoreToolkit(vectorstore_info=resource_vector_info)
        self.resource_agent_executor = create_vectorstore_agent(
            llm=self.llm, toolkit=resource_toolkit, verbose=True
        )

        example_toolkit = VectorStoreToolkit(vectorstore_info=example_vector_info)
        self.example_agent_executor = create_vectorstore_agent(
            llm=self.llm, toolkit=example_toolkit, verbose=True
        )

        resume_toolkit = VectorStoreToolkit(vectorstore_info=resume_vector_info)
        self.resume_agent_executor = create_vectorstore_agent(
            llm=self.llm, toolkit=resume_toolkit, verbose=True
        )
        
        print('created vectorstore router agent')

    async def specific_feedback(self, section, type):
        resume_clip = self.resume_agent_executor.run(f'return the exact section of the personal resume that is about {section}, word for word')
        # tutorial = self.resource_agent_executor(f'what is the best way of writing about {type}s, limit response to 50 words') # type = 'personal project', 'internship', 'award', etc..
        # example = self.example_agent_executor(f'give me an example of a {type}, word for word, limit response to 50 words')

        # feedback_1 = PromptTemplate(
        #     input_variables=['resume_clip','example'],
        #     template="Using the example: '{example}', rewrite the following part of a resume:'{resume_clip}'"
        # )
        # feedback_2 = PromptTemplate(
        #     input_variables=['resume_clip','tutorial'],
        #     template="Using the suggestion: '{tutorial}', further refine and reword the following part of a resume:'{resume_clip}'"
        # )

        # feedback_chain = LLMChain(llm=self.llm, prompt=feedback_1, verbose=True, output_key='edit1')
        # feedback_chain = LLMChain(llm=self.llm, prompt=feedback_2, verbose=True, output_key='edit2')

        # edit1 = feedback_chain.run(resume_clip=resume_clip, example=example)
        # edit2 = feedback_chain.run(resume_clip=resume_clip, tutorial=tutorial)

        feedback_2 = PromptTemplate(
            input_variables=['resume_clip'],
            template="improve and reword the following part of a resume:'{resume_clip}' using the star software engineering resume strategy"
        )
        feedback_chain = LLMChain(llm=self.llm, prompt=feedback_2, verbose=True, output_key='edit2')
        edit2 = feedback_chain.run(resume_clip=resume_clip)

        return edit2
    

            


