variable "sg_name" {
  type        = list(any)
  description = "Name of security groups that we make"
  default     = ["ecs", "rds"]
}