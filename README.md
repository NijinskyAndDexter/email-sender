# email-sender
used to send emails to me (privately) for personal website. Will be extended to accommodate needs of growing personal project over time. 


## set up steps
- install python3.9
- have the aws cli configured
- have make installed (mac users won't have to configure anything. For windows, the best way to run make is in an ubuntu terminal)
- run make deploy environment={your_environment_name} email_address={your_email_address}. I.E. `make deploy environment=dev email_address=fake@notanemail.com` this will deploy to the `dev` environment and deliver emails to the email address specified



