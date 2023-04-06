output "linux_instance_pub_ip" {
  value = aws_instance.linux_instance.public_ip
}

output "linux_instance_pvr_ip" {
  value = aws_instance.linux_instance.private_ip
}