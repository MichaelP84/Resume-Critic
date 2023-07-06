import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.vectorstores import Chroma
from langchain.agents.agent_toolkits import (
    create_vectorstore_router_agent,
    VectorStoreRouterToolkit,
    VectorStoreInfo
)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
print(os.environ["OPENAI_API_KEY"])

class Model():
    
    def __init__(self):
        self.llm = OpenAI(temperature=0.2, verbose=True)
        self.embeddings = OpenAIEmbeddings()
        self.agent_executor = None


    def get_resume_vs(self, resume_path):
        # read the pdf
        loader = UnstructuredPDFLoader(resume_path)
        # split the document up into array of pages
        pages = loader.load_and_split()
        # create Chroma vector storage
        store = Chroma.from_documents(pages, self.embeddings, collection_name='personal resume')
        resume_vector_info = VectorStoreInfo(
            name="personal_resume",
            description="A resume that needs to be critiqued, reworded, and improved as a pdf",
            vectorstore=store
            )

        return resume_vector_info
    
    def get_resource_vs(self, resources_path):
        # read the pdf
        loader = UnstructuredPDFLoader(resources_path)
        # split the document up into array of pages
        pages = loader.load_and_split()
        # create Chroma vector storage
        store = Chroma.from_documents(pages, self.embeddings, collection_name='resume resources')
        resource_vector_info = VectorStoreInfo(
            name="resources",
            description="A collection of tutorials about writing good software engineering resumes",
            vectorstore=store
            )

        return resource_vector_info
    
    def get_example_vs(self, resources_path):
        # read the pdf
        loader = UnstructuredPDFLoader(resources_path)
        # split the document up into array of pages
        pages = loader.load_and_split()
        # create Chroma vector storage
        store = Chroma.from_documents(pages, self.embeddings, collection_name='resume examples')
        example_vector_info = VectorStoreInfo(
            name="example",
            description="A collection of successful software engineering resumes",
            vectorstore=store
            )

        return example_vector_info

    def create_router_agent(self):
        resume_path = os.path.join('./resumes', os.listdir('./resumes')[0])
        resources_path = os.path.join('./resources', os.listdir('./resources')[0])
        
        resource_vector_info = self.get_resource_vs(resources_path)
        resume_vector_info = self.get_resume_vs(resume_path)

        router_toolkit = VectorStoreRouterToolkit(
            vectorstores=[resource_vector_info, resume_vector_info], llm=self.llm
        )
        self.agent_executor = create_vectorstore_router_agent(
            llm=self.llm, toolkit=router_toolkit, verbose=True
        )

            


