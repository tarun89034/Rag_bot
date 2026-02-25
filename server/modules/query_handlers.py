from logger import logger


def query_chain(chain, retriever, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")

        # Get the answer from the LCEL chain
        result = chain.invoke(user_input)

        # Get source documents from the retriever
        source_docs = retriever.invoke(user_input)

        response = {
            "response": result,
            "sources": [doc.metadata.get("source", "") for doc in source_docs]
        }
        logger.debug(f"Chain response: {response}")
        return response
    except Exception as e:
        logger.exception("Error in query_chain")
        raise