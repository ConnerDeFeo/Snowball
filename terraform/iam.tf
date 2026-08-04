# # Trust policy shared by every pod role.
# # sts:TagSession is required alongside sts:AssumeRole for EKS Pod Identity.
# data "aws_iam_policy_document" "pod_trust" {
#   statement {
#     effect  = "Allow"
#     actions = ["sts:AssumeRole", "sts:TagSession"]
#     principals {
#       type        = "Service"
#       identifiers = ["pods.eks.amazonaws.com"]
#     }
#   }
# }

# # DynamoDB access, one standalone policy per table so roles can mix and match.
# resource "aws_iam_policy" "dynamodb" {
#   for_each = {
#     documents         = aws_dynamodb_table.snowball_documents.arn
#     findings          = aws_dynamodb_table.snowball_findings.arn
#     section_grades    = aws_dynamodb_table.snowball_section_grades.arn
#     rubric_directions = aws_dynamodb_table.snowball_rubric_directions.arn
#     companies         = aws_dynamodb_table.snowball_companies.arn
#     review_sessions   = aws_dynamodb_table.snowball_review_sessions.arn
#   }
#   name = "snowball-dynamodb-${replace(each.key, "_", "-")}"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [{
#       Effect = "Allow"
#       Action = [
#         "dynamodb:GetItem",
#         "dynamodb:PutItem",
#         "dynamodb:Query",
#         "dynamodb:UpdateItem",
#         "dynamodb:DeleteItem",
#         "dynamodb:Scan"
#       ]
#       Resource = each.value
#     }]
#   })
# }

# # ---------------------------------------------------------------------------
# # analysis-pipeline: S3 (filing cache) + Bedrock (grading) + DynamoDB
# # ---------------------------------------------------------------------------

# resource "aws_iam_role" "analysis_pipeline" {
#   name               = "snowball-analysis-pipeline"
#   assume_role_policy = data.aws_iam_policy_document.pod_trust.json
# }

# resource "aws_iam_role_policy_attachment" "analysis_managed" {
#   for_each = toset([
#     "arn:aws:iam::aws:policy/AmazonS3FullAccess",
#     "arn:aws:iam::aws:policy/AmazonBedrockFullAccess",
#   ])
#   role       = aws_iam_role.analysis_pipeline.name
#   policy_arn = each.value
# }

# resource "aws_iam_role_policy_attachment" "analysis_dynamodb" {
#   for_each   = aws_iam_policy.dynamodb
#   role       = aws_iam_role.analysis_pipeline.name
#   policy_arn = each.value.arn
# }

# resource "aws_eks_pod_identity_association" "analysis_pipeline" {
#   cluster_name    = module.eks.cluster_name
#   namespace       = "default"
#   service_account = "analysis-pipeline"
#   role_arn        = aws_iam_role.analysis_pipeline.arn
# }

# # ---------------------------------------------------------------------------
# # review-pipeline: Bedrock (agent loop) + DynamoDB. No S3 until the vector
# # store lands.
# # ---------------------------------------------------------------------------

# resource "aws_iam_role" "review_pipeline" {
#   name               = "snowball-review-pipeline"
#   assume_role_policy = data.aws_iam_policy_document.pod_trust.json
# }

# resource "aws_iam_role_policy_attachment" "review_managed" {
#   for_each = toset([
#     "arn:aws:iam::aws:policy/AmazonBedrockFullAccess",
#   ])
#   role       = aws_iam_role.review_pipeline.name
#   policy_arn = each.value
# }

# resource "aws_iam_role_policy_attachment" "review_dynamodb" {
#   for_each   = aws_iam_policy.dynamodb
#   role       = aws_iam_role.review_pipeline.name
#   policy_arn = each.value.arn
# }

# resource "aws_eks_pod_identity_association" "review_pipeline" {
#   cluster_name    = module.eks.cluster_name
#   namespace       = "default"
#   service_account = "review-pipeline"
#   role_arn        = aws_iam_role.review_pipeline.arn
# }
