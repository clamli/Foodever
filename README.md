It is recommended that each of us maintains our own database and run website locally. By doing so, 1) we can test our app immediately without the need to deploy it on gcp first 2) our own bug will only happens in our environment

There are a few steps to set up the project to run on your localhost:8080

1. in **config.py** , find the variable called ``MONGODB_SETTINGS ``, set its value to ``{ 'host': 'mongomock://localhost' }``

Up until this point, you can already run the website on localhost, but 
we cannot upload our image to our own cloud storage. Other operations are good to go! 

2.  create a project on google app engine. You will find you **project id** at the Project Info. 
Then under **Resources** there should be a *storage** which says 2 buckets. Click on the storage, and find the bucket which has the name
``project id.appspot.com``, not the staging one.  

3. in **config.py**, find the variable ``PROJECT_ID``, set it to your project id

4. also in **config.py**, find ``CLOUD_STORAGE_BUCKET``, set its value to the bucket name
which is ``project id.appspot.com``

5. deploy this app from your computer by enter this directory and type ``gcloud app deploy``

Now feel free to experiment on your own! If have any questions, let us know in messages or wechat. 