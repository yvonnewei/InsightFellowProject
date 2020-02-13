## README.md
### Features

- A backend API to manage the access to database for different provider and patient groups which can efficiently increase the security level of sensitive data and customize access based on different roles
- Database schemas and rule tables with PostgreSQL and Django for user authentication and privileges

### Files in Repo
#### templates
Renders the information to be presented to the user. Including html pages, including home, patient_detail, and forbidden page

#### models.py
Creates role model for patient, contains the essential fields and behaviors of the data I storing. The patient model maps to a single database table.

#### permissions.py
Define permission rules

#### serializers.py
processing serializers

#### urls.py
create API endpoints

#### views.py
create view for each class

#### requirement.txt
package and environment required elements