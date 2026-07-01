from abc import ABC, abstractmethod
import random


class runnableClass(ABC):

    @abstractmethod
    def invoke(self, input_data):
        pass


class myLLM(runnableClass):

    def __init__(self):
        print("LLM is Created")

    def invoke(self, prompt):

        response_list = [
            "Artificial Intelligence is a branch of Computer Science.",
            "Capital of India is New Delhi.",
            "IPL is the Indian Premier League.",
            "Machine Learning is a subset of AI."
        ]

        print(f"\nLLM Prompt:\n{prompt}\n")

        randomIndex = random.randint(0, len(response_list) - 1)

        return {
            "response": response_list[randomIndex]
        }


class myPromptTemplate(runnableClass):

    def __init__(self, template, input_variables):
        print("Prompt Template is Created")
        self.template = template
        self.input_variables = input_variables

    def invoke(self, input_dict):
        return self.template.format(**input_dict)


class outputParser(runnableClass):

    def __init__(self):
        print("Output Parser is Created")

    def invoke(self, input_data):
        return input_data["response"]


class RunnableConnector(runnableClass):

    def __init__(self, runnables_list):
        self.runnables_list = runnables_list

    def invoke(self, input_data):

        result = input_data

        for runnable in self.runnables_list:
            result = runnable.invoke(result)

        return result


# --------------------------
# First Prompt
# --------------------------

template1 = myPromptTemplate(
    template="Write a {length} report on {topic}.",
    input_variables=["topic", "length"]
)

llm1 = myLLM()


# --------------------------
# Second Prompt
# Notice it uses {response}
# --------------------------

template2 = myPromptTemplate(
    template="Summarize the following report:\n\n{response}",
    input_variables=["response"]
)

llm2 = myLLM()

parser = outputParser()


chain = RunnableConnector([
    template1,
    llm1,
    template2,
    llm2,
    parser
])


print(
    chain.invoke(
        {
            "topic": "Artificial Intelligence",
            "length": "short"
        }
    )
)