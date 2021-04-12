# SOCIAL CONNECT
A simple social networking API backend where users can create, edit and/or delete posts.
A post has a title and body.

There are 3 kinds of users:
- General user
- Admin
- SuperAdmin

An admin can do all the CRUD operations on behalf of a user, if approved by superadmin.

In order to get permission for doing CRUD on behalf of user, an admin needs to raise a Access Request.

Only Superadmin can approve it.

Admin will get PermissionDenied error if no valid approved request is present.

Access Request expire after a time if not approved.

All requests and responses are logged.
Sensitive data is masked.


### Running the app
The app can be run in two ways, using `docker-compose` or `kubernetes`.

##### Docker-compose
- Clone the project.
- Run `docker-compose up --build` in the project root.

##### Kubernetes
- Install `minikube`, `KinD` or any other of your choice along with `kubectl`.
- Create a single node cluster.
- Clone the repo.
- Apply the manifests in PROJECT_ROOT/infra/k8s directory.
- Connect to the postgres pod and run PROJECT_ROOT/init.sql script.

###### Schema URL
`http://localhost:8000/schema/swaggerui/`

### Improvements needed for Production Deployment
- Robust User Management.
- More features.
- Add Tests.
- EKS instead of Minikube/KinD
- Private VPC.
- Better App logging.
- cAdvisor + Prometheus monitoring.
- Restrictions on Kibana Dashboard Access.
- Slack/Discord Integration.
