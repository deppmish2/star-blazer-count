## Process for Algorithm

#### Infra

Docker + Flask + python implementation comes naturally to me being in Machine Learning field since last 5 years.


#### Algorithm Approach

Aim was to look for simple and effective solution.
Looked into [here](https://docs.github.com/en/rest/reference/activity#list-repositories-starred-by-the-authenticated-user).
to understand how to list repositories starred by user.

Then I set up and ran simple flask app and tested it for few repositories using Postman to get total star count.
After that I went into drawing board where I normally use Miro to [visualize](https://github.com/deppmish2/star-blazer-count/blob/main/flowchart.jpeg) 
what actually the problem entails and how can i achieve the solution. 

The solution I came up was to have total star count for the repository and get total number of pages to get the complete history.
And call 100 items per page to achieve that as a default value.  

I am familier with using Pandas to generate, append and save a csv file.
I did the implementation and again tested using Postman for a few sample repos.

It did work but to improve the algorithm and make it faster (the average response times were quite high), I multithreaded 
the proceseses to fetch and save the data. Multithreading was a choice as the application requires heavy I/O bound operations.

Then the next step was to Dockerize the application and test it throughly again using Postman followed by Readme file.
Docker Containers allow to package up an application with all of the parts it needs, such as libraries and other 
dependencies, and ship it all out as one package. 


#### Time Constraints(4-6 hours) and Future Improvements

The major improvement lies in fetching data for Github repositories that have high number of stars (more than 1500). 

Another is to have maximum test coverage of the application with unit and integration test so that refactoring does not break anything and is 
robust solution in next versions.