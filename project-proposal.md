<!--
Fill out this document during Ship 3.
Describe which project track you are choosing (adventure game, password manager, or quiz app) and outline your ideas.
-->

## Project Proposal

**Chosen Track:** Password Manager

### Description

The program I want to build is a secure command-line password manager that solves the problem of users having to remember multiple passwords for different websites and services. Users will interact with the application through a command-line interface where they can register with a master password, store encrypted passwords for specific websites and services, and retrieve their stored passwords after authenticating with their master password.

For security, the master password will be hashed using a secure hashing algorithm in a JSON file. Individual passwords will be encrypted using the master password as a key before being stored. This approach ensures that even if the JSON file is compromised, the passwords remain protected without the master password. 

### Planned Features

The core features will include implementing the `register_user()` function to create new accounts with hashed master passwords and adding login functionality to authenticate users. The `add_password()` function will encrypt and store passwords for specific websites and services in a JSON database. The `get_passwords()` function will decrypt and display stored passwords after user authentication. The current greeting in `main()` will be replaced with a menu system allowing users to register, login, add passwords, and view stored passwords. Data persistence will be handled through JSON files to store user data and encrypted passwords, with proper error handling for file operations.

### Stretch Goals

Optional enhancements could include adding functionality to generate strong, random passwords with customizable length and character sets, implementing password strength checking to help users identify weak passwords, and allowing users to search for specific passwords by website name or username.