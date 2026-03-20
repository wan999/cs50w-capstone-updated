# NEWSPAPER WEBSITE UPDATED
#### Video Demo Updated: [Youtube Demonstration Video](https://youtu.be/nZTnhmXPnIU)
#### Description:
In this project I have made using Django a basic newspaper site to display information on current events / news. I've taken inspiration from various newspaper publisher websites such as 'The Guardian' and 'The New York Times'. Additionally I used a Bootstrap example (blog) to create this site. I used Bootstrap 4 to develop this project.

#### Distinctiveness and Complexity:
This website application has six different class models: Avatar, User, Category, Article, Comment, Editor and a Form class. The form class allows the user to upload a valid image file to use as a profile picture. For the image upload function to work the `PIL` python package needs to be installed. In addition, this website allows logged-in as well as anonymous users to comment on articles. I used a Javascript function to post these comments in `comments.js` with fetch 'POST'.

To view the `index.html` page the user does not have to be logged in. There are two user account types - public and editor accounts. Editors can publish articles which are published onto the site immediately as well as favorite articles. Public accounts can only favorite articles. Users can create an account and the admin superuser can add the user to the editor group which allows that user to publish articles. The editor user can delete their previously posted articles but cannot change the content of an article after it has been published. Each article displays the article content, article headline, category, timestamp, first and last name of the user who published said article, as well as a banner image. The articles are divided into categories so that the user can filter the articles by clicking on the keywords underneath the website title such as 'USA', 'Technology', 'World', 'Culture', etc.

The user can also search for articles by clicking on the search icon, which brings up a modal box. The user can search by typing in part of the article title, the search function is not case-sensitive.

The banner image used in the single view of each article is also used in the card view in `index.html`. The cards also display the article headline as well as a snippet of the first line of the article. 

The site is responsive and adapts to cellphone size screens with the layout of the cards changing to support the content on display. 

#### File Contents:
In the `media` folder are the profile images plus a default profile image in `media/static`.

In the `news/static` folder are the CSS styling files and Javascript files including `comments.js` and `modal.js`.

In the `news/templates` folder are the html templates used within this site.

In the `news/migrations` folder are the migration files.

### How To Run Application:
Install packages listed in requirements.txt file
 




