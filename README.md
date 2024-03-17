# VecinoVigilante - Crime Reporting Progressive Web Application

## Link to System Requirements

You can find the system requirements/project tickets on our Jira board: [VecinoVigilante Jira Board](https://vecinosvigilantes.atlassian.net/jira/software/projects/VV/boards/2)

## Description

VecinoVigilante is a progressive web application designed to keep citizens informed about complaints made near their location. It provides the following features:

- **Reporting Crimes:** Users can register locations where they have experienced or witnessed any crime.
- **Crime Map:** The application generates and displays a crime map that reflects the most dangerous sectors of the city.
- **Detailed Report Information:** Users can access detailed information on selected reports including description, type of crime, characteristics of suspects, date, and time.
- **User Contributions:** Other users can contribute additional information or comments on registered crimes.
- **Notification System:** Users receive notifications of new reports near their current location.

## Technologies Used

- Frontend: Flutter
- Backend: FastApi
- Database: MongoDB

## Commit Guidelines
When making commits, please follow these guidelines:

- **Format**: Commits follow [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) conventions followed by a Ticket number.
   For example if your ticket is TS123 then your commit would look like:
   ```
   feat: describe your changes (TS123)
   ```
   Allowed prefixes are:
   - `feat`: for a new feature for the user.
   - `fix`: for a bug fix for the user, not a fix to a build script.
   - `chore`: Changes to t auxiliary tools and libraries such as documentation generation
   - `ci`: Changes to CI/CD tools such as jenkins or github actions.
   - `docs`: for changes to the documentation.
   - `style`: for formatting changes, missing semicolons, etc (NOT CSS).
   - `refactor`: for refactoring production code, e.g. renaming a variable.
   - `perf`: for performance improvements.
   - `test`: for adding missing tests, refactoring tests; no production code change.
   - `build`: [RESERVED FOR RELEASES] for deploying new builds.

- **Atomic Commits:** Keep commits focused on a single logical change. Avoid bundling unrelated changes within a single commit.