#!/bin/bash
export AWS_DEFAULT_REGION=us-east-2

awslocal s3 mb s3://snowball-documents-bucket

awslocal dynamodb create-table \
  --table-name snowball_documents \
  --attribute-definitions AttributeName=accession,AttributeType=S \
  --key-schema AttributeName=accession,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

awslocal dynamodb create-table \
  --table-name snowball_findings \
  --attribute-definitions AttributeName=tckr,AttributeType=S AttributeName=finding_key,AttributeType=S \
  --key-schema AttributeName=tckr,KeyType=HASH AttributeName=finding_key,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

awslocal dynamodb create-table \
  --table-name snowball_section_grades \
  --attribute-definitions AttributeName=tckr,AttributeType=S AttributeName=category_period,AttributeType=S \
  --key-schema AttributeName=tckr,KeyType=HASH AttributeName=category_period,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

awslocal dynamodb create-table \
  --table-name snowball_rubric_directions \
  --attribute-definitions AttributeName=rubric_category,AttributeType=S AttributeName=sk,AttributeType=S \
  --key-schema AttributeName=rubric_category,KeyType=HASH AttributeName=sk,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

awslocal dynamodb create-table \
  --table-name snowball_companies \
  --attribute-definitions AttributeName=tckr,AttributeType=S \
  --key-schema AttributeName=tckr,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

awslocal dynamodb create-table \
  --table-name snowball_review_sessions \
  --attribute-definitions AttributeName=session_id,AttributeType=S \
  --key-schema AttributeName=session_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# LocalStack does not reliably enforce TTL expiry, but enabling it keeps
# behavior consistent with real AWS and is harmless either way.
awslocal dynamodb update-time-to-live \
  --table-name snowball_review_sessions \
  --time-to-live-specification "Enabled=true,AttributeName=expires_at"
