import csv
from langchain_ollama import ChatOllama

# Initialize the LLM
llm = ChatOllama(
    model="mistral:7b-instruct",
    temperature=0.5
)

def validate_with_llm(question, human_answer, llm_answer):
    """Validate the LLM's answer for level of correctness"""
    prompt = f"""
    You are an expert in evaluating the correctness of answers to trivia questions.
    Compare the llm's assessment with the correct answer and determine if the LLM did a good job at assessing the answer:
        1. Exact match
        2. Close match (semantically similar but not identical, and this can include typos or a partial match)
        3. Not a match
    Question: {question}
    Human Answer: {human_answer}
    LLM Answer: {llm_answer}
    Is the LLM's evaluation correct? Please respond with 'True' or 'False'.
    """
    
    response = llm.invoke(prompt)
    return response.content.strip()

def validate_results(csv_file, repetitions):
    """Validate the results of the quiz questions using the LLM multiple times"""
    for _ in range(repetitions):
        validation_results = []

        # Read the CSV file
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question = row['question']
                correct_answer = row['correct_answer']
                human_answer = row['human_answer']
                llm_result = row['llm_result']

                # Validate the LLM result
                llm_validation = validate_with_llm(question, human_answer, llm_result)

                # Compare with the correct answer
                is_correct = llm_validation == 'True' and llm_result == correct_answer

                # Log the result
                validation_results.append({
                    'question': question,
                    'correct_answer': correct_answer,
                    'human_answer': human_answer,
                    'llm_result': llm_result,
                    'llm_validation': llm_validation,
                    'is_correct': is_correct
                })

        # Write validation results to a new CSV file
        with open('validation_results.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['question', 'correct_answer', 'human_answer', 'llm_result', 'llm_validation', 'is_correct']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only once
            if csvfile.tell() == 0:
                writer.writeheader()
            for result in validation_results:
                writer.writerow(result)

# Run the validation with a specified number of repetitions
validate_results('functional_test_results.csv', 3)
