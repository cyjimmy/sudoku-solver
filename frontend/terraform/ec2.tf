resource "aws_key_pair" "ssh_key" {
  key_name   = "sudoku-solver"
  public_key = file("./.ssh/id_ed25519.pub")
}

resource "aws_instance" "linux_instance" {
  ami                         = "ami-04581fbf744a7d11f"
  iam_instance_profile        = aws_iam_instance_profile.ecs_agent.name
  vpc_security_group_ids      = [aws_security_group.sg[0].id]
  associate_public_ip_address = true
  instance_type               = "c4.8xlarge"
  subnet_id                   = aws_subnet.public[0].id
  key_name                    = aws_key_pair.ssh_key.key_name
  root_block_device {
    volume_size = 30
    volume_type = "gp2"
  }
}

resource "null_resource" "install-linux-tools" {
  connection {
    type        = "ssh"
    host        = aws_instance.linux_instance.public_ip
    user        = "ec2-user"
    port        = "22"
    private_key = file("./.ssh/id_ed25519")
    agent       = false
  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo amazon-linux-extras install mate-desktop1.x docker -y",
      "sudo bash -c 'echo PREFERRED=/usr/bin/mate-session > /etc/sysconfig/desktop'",
      "echo '/usr/bin/mate-session' > ~/.Xclients && chmod +x ~/.Xclients",
      "sudo yum install tigervnc-server -y",
      "sudo mkdir /home/ec2-user/.vnc",
      "sudo bash -c 'echo '123456' | vncpasswd -f > /home/ec2-user/.vnc/passwd'",
      "sudo chown -R ec2-user:ec2-user /home/ec2-user/.vnc",
      "sudo chmod 0600 /home/ec2-user/.vnc/passwd",
      "sudo mkdir /etc/tigervnc",
      "sudo bash -c 'echo localhost > /etc/tigervnc/vncserver-config-mandatory'",
      "sudo cp /lib/systemd/system/vncserver@.service /etc/systemd/system/vncserver@.service",
      "sudo sed -i 's/<USER>/ec2-user/' /etc/systemd/system/vncserver@.service",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable vncserver@:1",
      "sudo systemctl start vncserver@:1",
      "sudo aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 598490276344.dkr.ecr.us-east-1.amazonaws.com",
      "sudo systemctl enable docker",
      "sudo systemctl start docker",
      "sudo docker pull 598490276344.dkr.ecr.us-east-1.amazonaws.com/sudoku-solver:latest",
      "xhost",
      "xhost +local:docker",
      "sudo docker run -i -t -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw 598490276344.dkr.ecr.us-east-1.amazonaws.com/sudoku-solver:latest"
    ]
  }
}