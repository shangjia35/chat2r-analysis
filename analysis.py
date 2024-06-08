# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from scipy.stats import pearsonr
from matplotlib.font_manager import FontProperties
import numpy as np
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
#q14-15
chat2r_use_f = df.iloc[:, 19].dropna()
print(chat2r_use_f)
plt.title('Question 14: Chat2R Usage Frequency')
plt.pie(chat2r_use_f.value_counts(), labels=['Every week', 'Sometimes'])
plt.show()

whether_easy_to_use = df.iloc[:, 20].dropna()

plt.title('Question 15: Is Chat2R easy to use?')
plt.pie(whether_easy_to_use.value_counts(), labels=['Very easy', 'Easy', 'Medium'])
plt.show()
# %%
# q16-18
# eliminate rows where participants did not use chat2r
willingness_preselect = df[df.iloc[:, 18] != 2]
willingness_16_to_18 = willingness_preselect.iloc[:, [21, 22, 23]]
# print(willingness_16_to_18)


#q18
willingness_chat2r = df.iloc[:, 23]

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(willingness_chat2r.value_counts(), labels=['Very willing', 'willing', 'Medium', 'not willing'],
                                  autopct='%1.1f%%', startangle=140)
print(willingness_chat2r.value_counts())
# Add count numbers to the pie chart
for i, autotext in enumerate(autotexts):
    autotext.set_text(f'{sizes[i]} ({autotext.get_text()})')

# Equal aspect ratio ensures that pie is drawn as a circle.
ax.axis('equal')
plt.pie(willingness_chat2r.value_counts(), labels=['Very willing', 'willing', 'Medium', 'not willing'])
plt.show()
# %%
# GenAI willingness q19-24
for i in range(19, 25, 1):
    q = df.iloc[:, i + 5]
    print(f'Question {i} - Mean={q.mean()}, SD={q.std()}')

# plot all of them
genai_willingness = df.iloc[:, 24:30]
# print(genai_willingness)

willingness_mean = genai_willingness.mean()
# print(type(willingness_mean))
# print(willingness_mean)


# Create a bar plot
fig, ax = plt.subplots()
column_new_names = [f'Question {i}' for i in range(19, 25)]
values = willingness_mean.values
bars = ax.bar(willingness_mean.index, values)


# Add values on top of each bar
for bar, value in zip(bars, values):
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{value:.2f}', ha='center', va='bottom')

# Set new label names for categories
# ax.set_xticks(willingness_mean.index)  # Set the tick positions to the original category labels
ax.set_xticklabels([name for name in column_new_names], rotation=45, ha='right')  # Set the new labels

# Set title and labels
ax.set_title('Willingness Question 19-24 Mean Score')
ax.set_xlabel('Question number')
ax.set_ylabel('Mean score')

# Show plot
plt.show()

# willingness_mean.plot(kind='bar')
# column_new_names = [f'Question {i}' for i in range(19, 25)]
# plt.xlabel('Willingness Question Number')
# plt.ylabel('Mean Score')
# plt.title('Means for Each Willingness Question')
# plt.xticks(range(len(willingness_mean)), column_new_names)
# plt.xticks(rotation=45, ha='right')
# plt.show()

# %%
# columns_knowledge_llm q5-11 vs genai_willingness q19-24
knowledge_score_sum = columns_knowledge_llm.sum(axis=1)
knowledge_score_mean = knowledge_score_sum.mean()
willingness_score_sum = genai_willingness.sum(axis=1)
willingness_score_mean = willingness_score_sum.mean()

plt.scatter(knowledge_score_sum, willingness_score_sum)
plt.xlabel('knowledge score')
plt.ylabel('willingness score')
plt.grid(True)
plt.show()

# Calculate Pearson correlation coefficient and p-value
corr, p_value = pearsonr(knowledge_score_sum, willingness_score_sum)

print("Pearson correlation coefficient:", corr)
print("P-value:", p_value)
# %%
# q4 - majors
majors = df.iloc[:, 9]

font_path = '/System/Library/Fonts/STHeiti Medium.ttc'  # Change this to the correct path on your system
font_prop = FontProperties(fname=font_path)


value_counts = majors.value_counts()

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(value_counts, autopct='', startangle=140, textprops={'fontproperties': font_prop})

# Customize labels and percentages
for i, wedge in enumerate(wedges):
    angle = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
    y = np.sin(np.deg2rad(angle))
    x = np.cos(np.deg2rad(angle))

    if y > 0.98:
        y += 0.05
    
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(angle)
    
    ax.annotate(f'{value_counts.index[i]} ({value_counts[i]})',
                xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                horizontalalignment=horizontalalignment,
                fontsize=10, fontproperties=font_prop,
                arrowprops=dict(arrowstyle="->", connectionstyle=connectionstyle))
# plt.pie(majors.value_counts(), labels=majors.value_counts().index, autopct='%1.1f%%', startangle=140, textprops={'fontproperties': font_prop})
ax.axis('equal')
plt.title('Question 4: Majors', y=1.2)
plt.show()
# %%
# majors and knowledge_score_sum
distinct_majors = majors.unique()
print(distinct_majors)

# %%
# majors and willingness

#%%
# 1、对于学生背景的细致分析；2、每个问题的详细统计分析；3、问题间的相关性分析；4、对于使用chatbot问题的nlp分析，如：问题的类型、一个对话session中对话的轮次、不同背景学生使用chatbot情况的相关性分析