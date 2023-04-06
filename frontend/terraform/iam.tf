locals {
  assume_role_json = file("./policies/assume_role.tpl")
  permissions_json = file("./policies/permissions_policy.tpl")
}

resource "aws_iam_role" "ecs_cloudwatch" {
  count              = 1
  name               = "sudoku-solver"
  assume_role_policy = local.assume_role_json
  tags = {
    Name = "sudoku-solver"
  }
}

resource "aws_iam_role_policy" "ecs_cloudwatch" {
  count  = 1
  name   = "permissions-mitm-attack"
  policy = local.permissions_json
  role   = aws_iam_role.ecs_cloudwatch[0].name
}

resource "aws_iam_instance_profile" "ecs_agent" {
  name = "ecs-agent"
  role = aws_iam_role.ecs_cloudwatch[0].name
}