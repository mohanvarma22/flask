# Project Name: Flask Blog App with User Authentication and Content Management

Overview:
This project is a Flask-based web application that allows users to create, edit, and delete blog posts, manage their profiles, and perform user authentication. It incorporates database management, user roles, and a simple CMS (Content Management System) for blog content. The app is built using Flask, SQLAlchemy, and MySQL, with Flask-Migrate handling database migrations.

Features:
User Authentication and Authorization:

Users can register, login, and log out securely.
Passwords are hashed using werkzeug.security to ensure security.
Admin functionality: Admin users have additional privileges such as deleting any post or accessing admin-only pages.
User Profile Management:

Users can update their profiles with details like username, email, favorite color, and an "about author" section.
Profile deletion is restricted to users and administrators only.
Blog Post Management:

Authenticated users can add, edit, or delete their own posts.
Admin users can manage all posts.
Each post contains a title, slug, content, and a timestamp for when it was posted.
CKEditor integration provides rich text editing for blog content.
Post Search Functionality:

A search form allows users to search for posts by content.
Responsive Design:

The app is designed with responsiveness in mind, ensuring a smooth user experience across different devices.
