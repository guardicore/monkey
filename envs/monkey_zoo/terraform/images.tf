//Custom cloud images
data "google_compute_image" "hadoop-2" {
  name = "hadoop-2"
  project = local.monkeyzoo_project
}
data "google_compute_image" "hadoop-3" {
  name = "hadoop-3"
  project = local.monkeyzoo_project
}
data "google_compute_image" "elastic-4" {
  name = "elastic-4"
  project = local.monkeyzoo_project
}
data "google_compute_image" "elastic-5" {
  name = "elastic-5"
  project = local.monkeyzoo_project
}

/*
data "google_compute_image" "sambacry-6" {
  name = "sambacry-6"
}
*/
data "google_compute_image" "shellshock-8" {
  name = "shellshock-8"
  project = local.monkeyzoo_project
}
data "google_compute_image" "tunneling-9" {
  name = "tunneling-9"
  project = local.monkeyzoo_project
}
data "google_compute_image" "tunneling-10" {
  name = "tunneling-10"
  project = local.monkeyzoo_project
}
data "google_compute_image" "tunneling-11" {
  name = "tunneling-11"
  project = local.monkeyzoo_project
}
data "google_compute_image" "sshkeys-11" {
  name = "sshkeys-11"
  project = local.monkeyzoo_project
}
data "google_compute_image" "sshkeys-12" {
  name = "sshkeys-12"
  project = local.monkeyzoo_project
}
data "google_compute_image" "mimikatz-14" {
  name = "mimikatz-14"
  project = local.monkeyzoo_project
}
data "google_compute_image" "mimikatz-15" {
  name = "mimikatz-15"
  project = local.monkeyzoo_project
}
data "google_compute_image" "mssql-16" {
  name = "mssql-16"
  project = local.monkeyzoo_project
}
data "google_compute_image" "weblogic-18" {
  name = "weblogic-18"
  project = local.monkeyzoo_project
}
data "google_compute_image" "weblogic-19" {
  name = "weblogic-19"
  project = local.monkeyzoo_project
}
data "google_compute_image" "smb-20" {
  name = "smb-20"
  project = local.monkeyzoo_project
}
data "google_compute_image" "scan-21" {
  name = "scan-21"
  project = local.monkeyzoo_project
}
data "google_compute_image" "scan-22" {
  name = "scan-22"
  project = local.monkeyzoo_project
}
data "google_compute_image" "struts2-23" {
  name = "struts2-23"
  project = local.monkeyzoo_project
}
data "google_compute_image" "struts2-24" {
  name = "struts2-24"
  project = local.monkeyzoo_project
}
data "google_compute_image" "island-linux-250" {
  name = "island-linux-250"
  project = local.monkeyzoo_project
}
data "google_compute_image" "island-windows-251" {
  name = "island-windows-251"
  project = local.monkeyzoo_project
}
