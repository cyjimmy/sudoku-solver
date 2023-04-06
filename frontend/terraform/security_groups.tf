resource "aws_security_group" "sg" {
  count  = 2
  name   = "sudoku-solver-${var.sg_name[count.index]}"
  vpc_id = aws_vpc.vpc.id
}

resource "aws_security_group_rule" "ingress_ecs" {
  description       = "443 inbound, primary port"
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
  security_group_id = aws_security_group.sg[0].id
  type              = "ingress"
  cidr_blocks       = ["0.0.0.0/0"] #can be replaced with a restricted list of IPs but I'll ignore that here
}

resource "aws_security_group_rule" "ingress_rds_3306" {
  description       = "3306 inbound, default mySQL port"
  from_port         = 3306
  to_port           = 3306
  protocol          = "tcp"
  security_group_id = aws_security_group.sg[1].id
  type              = "ingress"
  cidr_blocks       = ["0.0.0.0/0"] #can be replaced with a restricted list of IPs but I'll ignore that here
}

resource "aws_security_group_rule" "egress" {
  count             = 2
  description       = "outbound 0. Allow ecs to access everything outside"
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
  security_group_id = aws_security_group.sg[count.index].id
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
}