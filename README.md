# IT Staffing Solutions

IT Staffing Solutions is a website that connects an employer and a candidate or job seeker. The employer will need to create an account to access all databases such as Employees, Timsheets and Jobs. The employer will be able to register a candidate by giving a unique ID, creating a timesheet and job advertisment. The registered candidate will be able to view their pay slip by entering their email and date of birth on the pay slip page. The job seeker will be able to apply for a job and receive a confirmation. The website allows the user to send an online form to the employer and receive a confirmation email. The below image shows how the databases are connected.
  
![db](registration/static/documents/db.png)
  
Employer successfully signed up
  
![emplosignup](registration/static/documents/employer-signup.png)
  
Employer successfully logged in
  
![empli](registration/static/documents/empli.png)

The employer entered incorrect data

![empliw](registration/static/documents/empliw.png)

The employer entered their email to reset the password

![emppr](registration/static/documents/emppr.png)

An email was sent to the employer to reset their password

![empprs](registration/static/documents/empprs.png)

The employer received the email to reset their password

![emppl](registration/static/documents/emppl.png)

The employer successfully reset the password

![emppf](registration/static/documents/emppf.png)

Employer registered an employee

![er](registration/static/documents/er.png) 

An employee was added to the database

![empad](registration/static/documents/empad.png)

The employee registration was rejected because the ID was given to another employee

![empn](registration/static/documents/empn.png) 

The employee registration was rejected because the ID was not a number

![empnot](registration/static/documents/empnot.png) 

The employer was asked to confirm deleting an employee

![eabd](registration/static/documents/eabd.png) 

The deletion was successful

![esde](registration/static/documents/esde.png)

The employer updated the employee's details

![esc](registration/static/documents/esc.png)

The employer created a timesheet

![ct](registration/static/documents/ct.png)

The timesheet was saved

![st](registration/static/documents/st.png)

The timesheet was not created

![tn](registration/static/documents/tn.png)

The timesheet was updated

![te](registration/static/documents/te.png)

The employer was asked to delete the timesheet

![td](registration/static/documents/td.png)

The timesheet was deleted

![tds](registration/static/documents/tds.png)

All stored pay slips

![ap](registration/static/documents/ap.png)

The candidate created an account

![esu](registration/static/documents/esu.png)

The candidate successfully signed up

![esus](registration/static/documents/esus.png)

The candidate successfully logged in

![csli](registration/static/documents/csli.png)

The candidate changed his profile

![cscp](registration/static/documents/cscp.png)

The candidate downloaded a file

![dfile](registration/static/documents/dfile.png)

The candidate accessed to the pay slip

![ep](registration/static/documents/ep.png)

The candidate entered the incorrect email to view the pay slip

![lip](registration/static/documents/lip.png)

The date of birth was incorrect to access the pay slip

![lipd](registration/static/documents/lipd.png)

The candidate successfully logged in to view the pay slip

![lps](registration/static/documents/lps.png)

The candidate downloaded the pay slip

![ppdf](registration/static/documents/ppdf.png)

A new job was created

![jf](registration/static/documents/jf.png)

The employer could not make a new job form because the reference was unique

![jn](registration/static/documents/jn.png)

The list of jobs

![jl](registration/static/documents/jl.png)

The job was deleted

![edj](registration/static/documents/edj.png)

Lateast job

![lj](registration/static/documents/lj.png)

The job details

![jdes](registration/static/documents/jdes.png)

The candidate applied for a job

![jm](registration/static/documents/jm.png)

The candidate received a confirmation email of the job application form

![jse](registration/static/documents/jse.png)

The employer received an email for a job submission form

![joe](registration/static/documents/joe.png)

The job seeker contacted the employer

![cf](registration/static/documents/cf.png)

The contact form submission was successful

![cfm](registration/static/documents/cfm.png)

The job seeker received a confirmation email about submitting an online form

![cfse](registration/static/documents/cfse.png)

The employer received an email from the job seeker

![cfoe](registration/static/documents/cfoe.png)

## Testing 
* In the base.html file, I created a section for an online form, some achievements of the practice and a button that helps the patient to make an appointment. I could use the ‘extends’ template tag to bring all the required codes to a child template or exclude a specific block if I wanted.  
* I had a problem with overlapping of contents in the project. Whenever I reduced the size of the screen, the appointment’s button which was in the header overlapped the telephone and email icons. The problem were repeated in every pages so I used a media query to fix the issue.   
* I created two tables which were adjacent to each other to show the costs of different treatments in the Fees & Finance page, but for a small screen, the right table overlapped the left one, so I changed the value of the property ‘Display’ to ‘Grid’ to fix the issue.  
* The Font Awesome icon did not appear on the position, although I included its link in the head section, so I tried another icon.   
* The first time, I used an external CSS style, but the style of the form, button and page were not changed so I used an internal CSS style which changed the appearance of the page. I found that I incorrectly wrote the path of CSS file, in the link tag.




## Unfixed bugs  
In the project, I used Django to send an email to the owner of the website and the user after submitting an online form. When I run a program at http://127.0.0.1:8000/, the owner and the user received the email.   
I also used PythonAnywhere to deploy the website which worked, but when the user submitted the online form, I received the below error, then when I went back to the previous page, the successful message of submitting the form was shown on the website. I was unable to fix this problem because I think I have a free account with them.





## Content  
* I got the contents of the site form Zental Dental Practice.  
* I used the Font Awsome icon for the dropdown menu and staff.  
* I used Google Font for the calendar icon.  
* W3Schools and AI generator helped with converting the design of the page from large screen to small screen.  

## Media  
*I used Google to get all images and logos.  
*The video is from You Tube.  
