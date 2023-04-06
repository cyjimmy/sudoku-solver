resource "aws_ecr_repository" "docker" {
  name = "sudoku-solver"
  image_tag_mutability = "MUTABLE"
  encryption_configuration {
    encryption_type = "KMS"
  }
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository_policy" "docker-policy" {
  repository = aws_ecr_repository.docker.id
  policy = <<EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "access policy",
              "Effect": "Allow",
              "Principal": {
                  "AWS": [
                      "arn:aws:iam::598490276344:root"
                  ]
              },
              "Action": "ecr:*"
          }
      ]
  }
  EOF
}