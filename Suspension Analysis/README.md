# Purpose

The college wanted to review its *academic suspension* and *probation* policies to see how students perform under the current conditions and whether those conditions are detrimental to student success long-term. Previous to the analysis, students on academic probation earned below a 2.0 GPA for a single semester, which limits them to no more than 12 credit hours. Students on academic suspension have earned two consecutive semesters of below 2.0 GPAs. The problem? Academic advisors have considerable leeway in how they enforce the rules. 

The official policy of the college is that students in their first semester of academic suspension can take no more than six credits, they have to be classes the student has previously failed, and they have to be in person. Nevertheless, this analysis revealed that we had a few academic advisors who were the main culprits of putting these students in 12 credits or more, which is a full-time work load. So we wanted to see what the effects of these disparate enforcements were on student success (defined as earning above a 2.0 in their semesters on academic probation or suspension). 

# The Data

The data is pulled from Oracle's Banner DB with SQL programming I write using PL/SQL. I pulled it for the last five academic years (AY). 

As always, the raw data files cannot be shared due to FERPA laws. 

## EDA

Each semester, there are about 11.00% of students who are put on either academic suspension or probation. About 60.00% of these students are probation, 40% are suspension. Depending on the semester, between 52.00% and as much as 62% of students who are on academic probation will take nine credits or more. Between 30.95% and 38.10% of students on academic probation will take 12 credits or more, a full time load. 

Suspension students, given their restrictions, enroll in fewer credit hours, on average. In fact, it is almost precisely flipped. Student on suspension, depending on the semester, will have between 54.00% and 60.00% of these students enrolled in six credits or less. 

# Results

The most shocking finding was that students on Academc Probation earn, on average, a considerably lower GPA than students who are on Academic Suspension. Probation students never eanred higher than a 1.40 GPA for any given semester examined. However, students on suspension never earned *lower than* a GPA Of 1.64. Probation students had one semester in which the *mean* GPA was 1.161. The highest GPAs for suspension students clustered around those who were enrolled in nine credits or less. 

## Action

Because of this analysis, the college changed its lax policy with a stricter policy for suspension students. The advisors who were putting students into 12 credits or more while on suspension were directly spoken with and the entire staff was addressed to explain just what is at stake when these students are put into too many credits. The harder policy to change is the one related to probation students. At present, probation students continue to be allowed to be in 12 credits rather than limiting them to 9 credits. 

The current proposal is to reduce these students' options which carries both a psychological effect as well as a (hopefully) positive effect. The pyschological effect is that the students have a stronger sense that it is not "business as usual." Things are not going well. The positive effect is that fewer credits will (hopefully) translate into more time on task for the courses in which they are enrolled. 
