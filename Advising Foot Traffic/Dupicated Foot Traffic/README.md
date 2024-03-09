# Purpose

This analysis was a secondary analysis to the Academic Advising Foot Traffic analysis to isolate and control for duplicate entrees. Part of the goal for this for the Director of Advising and the VP of Enrollment Management is to have an accurate view of the distribution of workload throughout the department. Unfortunately, there is not uniform execution of entries. In the old days, nearly all students, with very rare exception, had to walk in to the advising office to be assisted with enrollment. We always assisted students with questions over the phone and via email, but enrollment was reserved only for walk-in students. After COVID, this all changed. Students can enroll in-person, via email, phone call, or Zoom now. The later three of these require the advisor to enter the student's name into the sign-in sheet. 

This results in wild disparities between advisors. Some advisors will enter a student they assit remotely (Zoom, email, phone) only once or not at all. Others will enter a student every time they interact with that student, which causes many duplicate entiries within a single week. Conequently, this makes accurate assessment of workload very difficult. Therefore, this analysis controls for duplicate entrees to reveal a more realistic view of each Advisor's work.

# The Data

Once again, the data included here, even though it is the advising sign-in sheet, cannot be included in its raw form due to FERPA laws. 

Teh data was pulled from our sign-in sheets and then I cleaned it to be used for analysis. The raw form of the data is in no way ready for analysis. Missing dates, wrong data formats, and simple 'x' to indicate a category all need to be cleaned and programmed for meaning. 

# Results

This was a fairly strait-forward programming task. I did not need any ML modeling. Just a quick analysis. The benefit of the code I wrote here is that it can be ran at any time with new data in seconds to reveal the same insights. 

As a result of this analysis, the Director of Advising made it so that all advisors were linked to the academic advising email. This analysis revealed that the two advisors who were overseeing that email had a tremendous workload, which was causing undue strife. Therefore, all advisors were put on that email to relieve the workload and distribute it more evenly. 
