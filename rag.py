from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from .vector_store import load_vector_store


def get_rag_chain():

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite"
    )

    prompt = ChatPromptTemplate.from_template(
        """
        You are an Enterprise Knowledge Assistant.

        Answer the user's question using ONLY the provided context.

        If the answer cannot be found in the context, say:

        "I could not find this information in the provided documents."

        Keep the answer clear and concise.

        Context:
        {context}

        Question:
        {question}
        """
    )

    def ask_question(question):

        documents = retriever.invoke(question)

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        messages = prompt.invoke(
            {
                "context": context,
                "question": question
            }
        )

        response = llm.invoke(messages)

        if isinstance(response.content, list):

            answer = "\n".join(
                item.get("text", "")
                for item in response.content
                if isinstance(item, dict)
            )

        else:

            answer = str(response.content)

        sources = list(
            dict.fromkeys(
                document.metadata.get(
                    "source",
                    "Unknown"
                )
                for document in documents
            )
        )

        return answer, sources

    return ask_question