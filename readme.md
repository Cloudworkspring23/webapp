Building Rest API using Python. MySQL and Flask

This is a python web application for storing the user information into MySQL database.

User input is taken from Postman

User passwords are encrypted with BCrypt hashing and salt in the database

Authentication is done using basic auth

This API implements GET,POST,PUT and Delete methods

The infrasturucture files ami.pkr.hcl is used to create custom AMI with all the dependency required to build and start the web application. The AMI file is automatically build in the GitHub action workflows.


Call the API using Postman
User input is taken from Postman
packer
```

> NOTE: If you get an error that packer could not be found, then your PATH environment variable was not set up properly. Please go back and ensure that your PATH variable contains the directory which has Packer installed. Otherwise, Packer is installed and you're ready to go!

### :wrench: Building Custom AMI using Packer

Packer uses Hashicorp Configuration Language(HCL) to create a build template. We'll use the [Packer docs](https://www.packer.io/docs/templates/hcl_templates) to create the build template file.

> NOTE: The file should end with the `.pkr.hcl` extension to be parsed using the HCL2 format.

#### Create the `.pkr.hcl` template

The custom AMI should have the following features:

> NOTE: The builder to be used is `amazon-ebs`.

- **OS:** `Ubuntu 22.04 LTS`
- **Build:** built on the default VPC
- **Device Name:** `/dev/sda1/`
- **Volume Size:** `50GiB`
- **Volume Type:** `gp2`
- Have valid `provisioners`.
- Pre-installed dependencies using a shell script.
- Web application software pre-installed on the AMI.

#### Shell Provisioners

This will automate the process of updating the OS packages and installing software on the AMI and will have our application in a running state whenever the custom AMI is used to launch an EC2 instance. It should also copy artifacts to the AMI in order to get the application running. It is important to bootstrap our application here, instead of manually SSH-ing into the AMI instance.

Install application prerequisites, middlewares and runtime dependencies here. Update the permission and file ownership on the copied application artifacts.

> NOTE: The file provisioners must copy the application artifacts and configuration to the right location.

#### Custom AMI creation

To create the custom AMI from the `.pkr.hcl` template created earlier, use the commands given below:

- If you're using Packer plugins , run the `init` command first:

```shell
# Installs all packer plugins mentioned in the config template
packer init .
```

- To format the template, use:

```shell
packer fmt .
```

- To validate the template, use:

```shell
# to validate syntax only
packer validate -syntax-only .
# to validate the template as a whole
packer validate -evaluate-datasources .
```

- To build the custom AMI using packer, use:

```shell
packer build <filename>.pkr.hcl
```

#### Packer HCL Variables

To prevent pushing sensitive details to your version control, we can have variables in the `<file-name>.pkr.hcl` file, and then declare the actual values for these variables in another HCL file with the extension `.pkrvars.hcl`.

If you want to validate your build configuration, you can use the following command:

```shell
packer validate -evaluate-datasources --var-file=<variables-file>.pkrvars.hcl <build-config>.pkr.hcl
```

> NOTE: To use the `-evaluate-datasources` parameter, you'll have to update packer to `v1.8.5` or greater. For more details, refer [this issue](https://github.com/hashicorp/packer/issues/12056).

To use this variables files when creating a golden image, use the build command as shown:

```shell
packer build --var-file=<variables-file>.pkrvars.hcl <build-config>.pkr.hcl
```

> NOTE: Using variables is the preferred way/best practice to build a custom AMI using HCP Packer!

#### [systemd](https://systemd.io/)

`systemd` is a suite of basic building blocks for a Linux system. It provides a system and service manager that runs as PID 1 and starts the rest of the system.. This will help us bootstrap our application and have it in a running state when we launch our custom AMI EC2 instance using the CloudFormation stack.

For a detailed example, please refer [this ShellHacks blog](https://www.shellhacks.com/systemd-service-file-example/).

## :arrows_clockwise: CI/CD pipelines

### Unit tests

This CI pipeline must run before changes are merged via a PR to the upstream master branch. Once the unit tests pass, the CI pipeline should check the validity of the packer build configuration.

### Validate template

This CI pipeline will validate the packer build template when a pull request is opened. The PR status checks should fail and block merge in case the template is invalid.

### Build AMI

This is the CD pipeline for our organization.

The AMI should be built when the PR is merged. The ami should be shared with the AWS `prod` account automatically. [This can be done by providing the AWS account ID in the packer template, [see here](https://developer.hashicorp.com/packer/plugins/builders/amazon/ebs#ami_users)].

Create the `.env` file on the fly, when unpacking artifacts! You will need to declare the environment secrets in the organization secrets, and read them during the CI/CD workflow.

After the AMI is built, we will create a new version of the launch template and update the original launch template. With this latest version of the launch template, we will issue an `instance-refresh` command that will update the instances running in our CloudFormation stack to use the latest version of the launch template.

Using the `instance-refresh` approach, we are just replacing the golden image in our app infra where instances using an older golden image are sacked, and new instances are launched using the latest golden image(AMI).