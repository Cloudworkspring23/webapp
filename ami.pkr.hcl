
variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "us-east-1"
}

variable "source_ami" {
  type        = string
  description = "Default Ubuntu AMI to build our custom AMI"
  default     = "ami-065bb5126e4504910" #Ubuntu 22.04 LTS
}

variable "ami_prefix" {
  type        = string
  description = "AWS AMI name prefix"
  default     = "ami_prefix"
}

variable "ssh_username" {
  type        = string
  description = "username to ssh into the AMI Instance"
  default     = "ec2-user"
}

variable "subnet_id" {
  type        = string
  description = "Subnet of the default VPC"
  default     = "subnet-0017f659b92738c3b"
}

variable "OS" {
  type        = string
  description = "Base operating system version"
  default     = "OS"
}

variable "instance_type" {
  type        = string
  description = "AWS AMI instance type"
  default     = "t2.micro"
}
variable "volume_type" {
  type        = string
  description = "EBS volume type"
  default     = "gp2"
}
variable "volume_size" {
  type        = string
  description = "EBS volume size"
  default     = "50"
}
variable "device_name" {
  type        = string
  description = "EBS device name"
  default     = "/dev/sda1"
}
variable "ak" {
  type        = string
  description = "AWS access key"
  default     = "AKIASXMHSEK4DU7J4JD4"
}
variable "sk" {
  type        = string
  description = "AWS security_key"
  default     = "q8albyM3pkr3L2oQLw6lmyaTRHQK67eQCieOpuJF"
}

source "amazon-ebs" "my-ami" {
  region          = "${var.aws_region}"
  ami_name        = "cloud_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  ami_description = "AMI for cloud assignments"
  access_key = "${var.ak}"
  secret_key = "${var.sk}" # dev account ID # prod account ID
  

  ami_regions = [
    "us-east-1",

  ]
  aws_polling {
    delay_seconds = 120
    max_attempts  = 50
  }
  #instance
  instance_type = "t2.micro"
  source_ami    = "${var.source_ami}"
  ssh_username  = "${var.ssh_username}"
  subnet_id     = "${var.subnet_id}"

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/xvda"
    volume_size           = 8
    volume_type           = "gp2"
  }
}

build {
  sources = ["source.amazon-ebs.my-ami"]

  provisioner "file" {
    source      = "webapp.zip"                # path in local system to a tar.gz file
    destination = "/home/ec2-user/webapp.zip" # path in the AMI to store the webapp
  }
  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1"
    ]
    scripts = [
      "install.sh",
    ]
  }

}