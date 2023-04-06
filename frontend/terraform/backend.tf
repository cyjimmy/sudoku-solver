terraform {
  backend "s3" {
    bucket  = "sudoku-solver-manjot"
    key     = "state.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}