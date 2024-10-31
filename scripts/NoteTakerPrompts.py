ANTHROPIC_PROMPTS = {
    # Add version and metadata
    "_metadata": {
        "version": "1.0.0",
        "last_updated": "2024-10-30",
        "author": "Anatolii Kalinin",
    },
    "executive_summary": {
        "system": """You are an expert academic assistant specializing in creating clear, concise executive summaries of engineering lectures. You excel at identifying key concepts and presenting them in a structured format.""",
        "user": """Create an executive summary of this engineering lecture transcript:
<lecture_transcript>
{transcript}
</lecture_transcript>

Requirements:

    Content:
        1. Provide one paragraph (5-10 sentences).
        2. Encapsulate the essence of the lecture. Focus on main topics and key concepts
        3. Use clear, concise language.
        4. Include only relevant information.
        5. Convert ALL mathematical expressions to LaTeX notation
    
    Format:
        1. Use consistent HTML formatting.
        2. Start with <h1>Executive Summary</h1> heading.
        3. DO NOT use lists, bullet points, or numbered items. Write in full sentences.
        4. Use <b>tags</b> for key terms.
        5. Use LaTeX $...$ for inline math.
        6. Use LaTeX $$...$$ for display math.

    Think before you output the executive summary in <thinking> tags. First, think about what main concepts were discussed in the lecture. Think about the progression of the lecture and how to organize the summary effectively to capture this progression while adhering to the guidelines. Then, think about how to encapsulate the essence of the lecture in a concise and informative way that will benefit the students. Finally, review all the guidelines and requirements and come up with a plan to ensure your output meets the necessary criteria.
    
    Your final output should look like this:

    <thinking>[Your thinking here]</thinking>
    <h1>Executive Summary</h1> 
    <p>[Your concise summary here]</p>

Remember to STRICTLY ADHERE to all content and formatting guidelines provided above. This is crucial for providing accurate and high-quality output for the students.
Begin your analysis and provide the formatted output now.
""",
        "assistant": "<thinking>",
        "temperature": 0.2,
    },
    "key_points": {
        "system": """You are an expert academic assistant specializing in extracting and organizing key information from engineering lectures. You excel at identifying main concepts and action items.""",
        "user": """Extract key points and action items from this engineering lecture transcript:
<lecture_transcript>
{transcript}
</lecture_transcript>

Requirements:

    Content:
        1. Your output MUST contain ONLY two main sections: Key Points and Action Items.
        2. Include ALL the relevant key points and action items from the lecture.
        3. Key Points and Action Items should be listed in the chronologicl order.
        4. Include only the action items mentioned explicitly by the lecturer.
        5. Omit any irrelevant information. Use clear, concise language.
    
    Formatting Guidelines:
        1. Use consistent HTML formatting.
        2. SUse <h1>Main</h1> as the title.
        3. Create two sections: <h2>Key Points</h2> and <h2>Action Items</h2>
        4. List items using ONLY <ul> and <li> tags
        5. Enclose important words, phrases, and concepts in <b></b> tags.
        6. Use LaTeX $...$ for inline math
        7. Use LaTeX $$...$$ for display math

    Think before you output the key points and action items in <thinking> tags:
        1. Think about what main concepts were discussed in the lecture.
        2. Think about how to summarize these concepts into key points effectively, encapsulating the essence of the lecture.
        3. Think about what tasks or assignments the lecturer mentioned that students should do after the lecture.
        4. Recall the guidelines for formatting equations and mathematical expressions; give an example.
        5. Finally, review all the guidelines and requirements and come up with a plan to ensure your output meets the necessary criteria.

    Format your response exactly as:
    <thinking>[thinking goes here]</thinking>
    <h1>Main</h1>
    <h2>Key Points</h2>
    <ul>
    [key points here]
    </ul>
    <h2>Action Items</h2>
    <ul>
    [action items here]
    </ul>

Remember to STRICTLY ADHERE to all content and formatting guidelines provided above. This is crucial for providing accurate and high-quality output for the students.
Begin your analysis and provide the formatted output now.
 """,
        "assistant": "<thinking>",
        "temperature": 0.2,
    },
    "detailed_notes": {
        "system": """You are an expert academic assistant specializing in creating comprehensive engineering lecture notes. You excel at organizing complex technical content into clear, structured documentation.""",
        "user": """Create detailed notes from this lecture transcript:
<lecture_transcript>
{transcript}
</lecture_transcript>

Requirements:
    Content:
        1. Cover ALL concepts chronologically.
        2. Include ALL equations, formulas, derivations, explanations, and examples.
        3. Explain complex concepts in <i>(Concept Explained: ...)</i> format.
        4. Mark inferred content with <i>(generated from context)</i>
        5. Mark knowledge-based additions with <i>(generated from knowledge)</i>
        6. Convert ALL mathematical expressions to LaTeX notation.
        7. Ensure notes are easy to read and follow.
        8. Use clear, concise, and professional language. Avoid ambiguity.

    Organization:
        1. Number main topics sequentially.
        2. Use complete senteces and paragraphs.
        3. Maintain clear topic progression.
        4. Organize notes into main topics, subtopics, sub-subtopics, and so on, where necessary.
            
    Formatting Guidelines:
        1. Use consistent HTML formatting throughout the notes.
        2. Start with <h1>Detailed Notes</h1>
        3. Use the following HTML tags for headings:
            - Main topics: <h2></h2>
            - Subtopics: <h3></h3>
            - Sub-subtopics: <h4></h4>
            - Further subdivisions: Continue with appropriate heading tags
        4. Enclose important words, phrases, and concepts in <b></b> tags.
        5. Use LaTeX $...$ for inline math
        6. Use LaTeX $$...$$ for display math
            
    Think before you output the detailed notes in <thinking> tags. First, think about what main concepts were discussed in the lecture. Think about the progression of the lecture and how to organize the content effectively to capture this progression while adhering to the guidelines. Then, think about what information in the lecture transcript was missing and why. Were there any clues that were not represented in the transcript? Were some concepts forgotten? Finally, Think about how to fill in all these gaps effectively and accurately so that students reading these notes will be able to understand and recall the entire content. Finally, review all the guidelines and requirements and come up with a plan to ensure your output meets the necessary criteria.
        
    Your final output should look like this:
        
    <thinking>[thinking goes here]</thinking>
    <h1>Detailed Notes</h1>
    <h2>1. [First Main Topic]</h2>
    <p>[content]</p>
    <h3>1.1 [Subtopic]</h3>
    <p>[content]</p>
    ...
    <h2>2. [Second Main Topic]</h2>
    <p>[content]</p>
    ...

Remember to STRICTLY ADHERE to all content and formatting guidelines provided above. This is crucial for providing accurate and high-quality output for the students.
Begin your analysis and provide the formatted output now.
""",
        "assistant": "<thinking>",
        "temperature": 0.3,
    },
    "study_guide": {
        "system": """You are an expert academic instructor specializing in creating comprehensive study guides for engineering courses. You excel at explaining complex concepts and creating practice problems.""",
        "user": """Create a study guide from this engineering lecture transcript:
<lecture_transcript>
{transcript}
</lecture_transcript>

Requirements:
    
    Content:
        1. Create a study guide that covers ALL concepts mentioned in the lecture.
        2. Organize the study guide into main topics, subtopics, sub-subtopics, and so on, where necessary.
        3. Provide clear, step-by-step explanations for all the concepts discussed in the lecture.
        4. Include brief descriptions of any visual aids or diagrams mentioned in the lecture.
        5. If applicable, include a section on practical applications or examples of the concepts discussed.
        6. Add a <h2>Practice Problems</h2> section with 4 example problems.
        7. Add a <h2>Practice Problems Solutions</h2> section with solutions to the practice problems.
        8. Add a <h2>Further Study</h2> section at the end, suggesting related topics and additional resources for deeper understanding.
        9. Ensure the guide is comprehensive yet concise and suitable for review and self-study.
        10. DO NOT copy the transcript verbatim. Use your knowledge to provide a comprehensive study guide.
        11. Convert ALL mathematical expressions to LaTeX notation.

    Formatting Guidelines:
        1. Use consistent HTML formatting.
        2. Start with <h1>AI Lecture Study Guide</h1>.
        3. Use <h2> for main sections
        4. Use <h3> for sub-sections.
        5. Enclose important words, phrases, and concepts in <b></b> tags.
        6. Use LaTeX $...$ for inline math
        7. Use LaTeX $$...$$ for display math

            
    Think before you write the study guide in <thinking> tags. First, think about what concepts were discussed in the lecture and how you can best explain them in the study guide in the most effective way. Consider what additional concepts students might need to understand the lecture better and more effectively. Then, think about the structure of the study guide and how to organize the content effectively while adhering to the guidelines. Finally, think about how to provide practical examples and problems to help students apply the concepts. Finally, review all the guidelines and requirements and come up with a plan to ensure your output meets the necessary criteria.

    Format your response starting with:
    <thinking>[thinking goes here].</thinking>
    <h1>AI Lecture Study Guide</h1>
    <p>[content]</p>
    <h2>1 [First Main Topic]</h2>
    <p>[content]</p>
    <h3>1.1 [First Subtopic]</h3>
    <p>[content]</p>
    ...
    <h2>2 [Second Main Topic]</h2>
    <p>[content]</p>
    ...
    <h2>Practice Problems</h2>
    <p>[content]</p>
    <h2>Practice Problems Solutions</h2>
    <p>[content]</p>
    <h2>Further Study</h2>
    <p>[content]</p>

Remember to STRICTLY ADHERE to all content and formatting guidelines provided above. This is crucial for providing accurate and high-quality output for the students.
Begin your analysis and provide the formatted output now.
 """,
        "assistant": "<thinking>",
        "temperature": 0.4,
    },
}


if __name__ == "__main__":

    print(ANTHROPIC_PROMPTS["study_guide"]["assistant"])
    pass
