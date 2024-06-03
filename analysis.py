# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
# %%
# read in file
file_path = '261102387_按序号_医学数据挖掘实用技术课程Chatbot使用反馈调查_32_32.xlsx'
df = pd.read_excel(file_path)
# %%
# knowledge questions q5-q11
columns_knowledge_llm = df.iloc[:, 10:17]
knowledge_means = columns_knowledge_llm.mean()

knowledge_means.plot(kind='bar')
column_new_names = [f'Question {i}' for i in range(5, 12)]
plt.xlabel('Knowledge Question Number')
plt.ylabel('Mean Score')
plt.title('Means for Each Knowledge Question')
plt.xticks(range(len(knowledge_means)), column_new_names)
plt.xticks(rotation=45, ha='right')
plt.show()

knowledge_score_sum = columns_knowledge_llm.sum(axis=1)
knowledge_score_mean = knowledge_score_sum.mean()
# print(columns_knowledge_llm)
# print(knowledge_score_sum)
# print(knowledge_score_mean)
# %%
# The relationship between q12 and q13
whether_used_genai = df.iloc[:, 17]
plt.title('Question 12: Whether have used GenAI before?')
plt.pie(whether_used_genai.value_counts(), labels=['Yes', 'No'])
plt.show()

whether_used_chat2r = df.iloc[:, 18]
plt.title('Question 13: Whether used Chatbot in class?')
plt.pie(whether_used_chat2r.value_counts(), labels=['Yes', 'No'])
plt.show()

contingency_table = pd.crosstab(whether_used_genai, whether_used_chat2r)
chi2, p, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-squared statistic: {chi2}")
print(f"P-value: {p}")
alpha = 0.05
if p < alpha:
    print("Reject the null hypothesis: There is a significant association between the variables.")
else:
    print("Fail to reject the null hypothesis: No significant association between the variables.")
# %%
