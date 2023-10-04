variable "project_id" {
  type = string
}
variable "zone" {
  type    = string
  default = "europe-west1-b"
}
variable "machine_type" {
  type    = string
  default = "e2-standard-4"
}
variable "windows_source_image" {
  type    = string
  default = "windows-server-2016-dc-v20211216"
}
variable "linux_source_image" {
  type    = string
  default = "ubuntu-2004-focal-v20230907"
}
variable "account_file" {
  type = string
}
variable "packer_username" {
  type    = string
  default = "packer_user"
}
variable "packer_user_password" {
  type    = string
  default = "Passw0rd"
}
