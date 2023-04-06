resource "aws_vpc" "vpc" {
  cidr_block           = "100.100.100.0/24"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "sudoku-solver"
  }
}

resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name = "sudoku-solver"
  }
}

#keep to 1 but might change later
resource "aws_subnet" "public" {
  count      = 1
  vpc_id     = aws_vpc.vpc.id
  cidr_block = cidrsubnet(aws_vpc.vpc.cidr_block, 2, 1 + count.index)
  tags = {
    Name = "sudoku-solver"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name = "sudoku-solver"
  }
}

resource "aws_route_table_association" "route_table_association" {
  count          = length(aws_subnet.public.*.id)
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}