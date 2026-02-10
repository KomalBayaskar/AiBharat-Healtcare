"""
Healthcare AI Assistant - AWS Architecture Diagram Generator
Run this script to generate the architecture diagram as a PNG file.
"""

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.database import Dynamodb, RDS
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito, WAF, Guardduty
from diagrams.aws.management import Cloudwatch, Cloudtrail
from diagrams.aws.integration import Appsync
from diagrams.aws.ml import Bedrock, Sagemaker, Comprehend
from diagrams.onprem.client import User
from diagrams.aws.general import InternetGateway

# Configure diagram
graph_attr = {
    "fontsize": "12",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram("Healthcare AI Assistant Architecture", 
             show=False, 
             direction="LR",
             filename="generated-diagrams/healthcare-ai-architecture",
             graph_attr=graph_attr):
    
    # Users
    healthcare_pro = User("Healthcare\nProfessional")
    patient = User("Patient")
    
    # Frontend & CDN
    with Cluster("Frontend Layer"):
        cloudfront = CloudFront("CloudFront CDN")
        s3_web = S3("Web App\n(React/Vue)")
    
    # Security
    waf = WAF("WAF")
    cognito = Cognito("Cognito\nAuth")
    
    # API Layer
    api_gateway = APIGateway("API Gateway")
    appsync = Appsync("GraphQL API")
    
    # Application Layer
    with Cluster("Application Layer (Serverless)"):
        lambda_clinical = Lambda("Clinical\nSummarizer")
        lambda_patient = Lambda("Patient\nNavigator")
        lambda_docs = Lambda("Documentation\nAssistant")
    
    # AI/ML Services
    with Cluster("AI/ML Services"):
        bedrock = Bedrock("Amazon Bedrock\n(Claude/Titan)")
        sagemaker = Sagemaker("SageMaker\nCustom Models")
        comprehend = Comprehend("Comprehend\nMedical")
    
    # Data Storage
    with Cluster("Data Storage"):
        dynamodb = Dynamodb("DynamoDB\nSessions/Audit")
        s3_data = S3("S3\nKnowledge Base")
        rds = RDS("Aurora RDS\nTemplates")
    
    # Monitoring & Security
    with Cluster("Monitoring & Compliance"):
        cloudwatch = Cloudwatch("CloudWatch")
        cloudtrail = Cloudtrail("CloudTrail")
        guardduty = Guardduty("GuardDuty")
    
    # External Sources
    with Cluster("External Medical Sources"):
        pubmed = InternetGateway("PubMed API")
        medical_db = InternetGateway("Medical DBs")
    
    # User flows
    healthcare_pro >> cloudfront
    patient >> cloudfront
    cloudfront >> s3_web
    
    # Security flow
    s3_web >> waf >> api_gateway
    api_gateway >> cognito
    
    # API routing
    api_gateway >> appsync
    appsync >> [lambda_clinical, lambda_patient, lambda_docs]
    
    # AI/ML integration
    lambda_clinical >> bedrock
    lambda_patient >> bedrock
    lambda_docs >> bedrock
    
    lambda_clinical >> sagemaker
    lambda_clinical >> comprehend
    
    # Data access
    lambda_clinical >> dynamodb
    lambda_patient >> dynamodb
    lambda_docs >> dynamodb
    
    lambda_clinical >> s3_data
    lambda_patient >> s3_data
    lambda_docs >> rds
    
    # External data sources
    lambda_clinical >> Edge(label="Fetch Literature") >> pubmed
    lambda_clinical >> Edge(label="Query Guidelines") >> medical_db
    
    # Security monitoring
    api_gateway >> guardduty
    lambda_clinical >> cloudtrail
    lambda_patient >> cloudtrail
    lambda_docs >> cloudtrail
    
    # Monitoring
    lambda_clinical >> cloudwatch
    lambda_patient >> cloudwatch
    lambda_docs >> cloudwatch

print("✓ Architecture diagram generated successfully!")
print("✓ File saved as: generated-diagrams/healthcare-ai-architecture.png")
print("\nArchitecture Overview:")
print("- Frontend: CloudFront + S3 static website")
print("- Security: WAF + Cognito + GuardDuty")
print("- API: API Gateway + AppSync GraphQL")
print("- Compute: 3 Lambda functions (serverless)")
print("- AI/ML: Bedrock + SageMaker + Comprehend Medical")
print("- Storage: DynamoDB + S3 + Aurora RDS")
print("- Monitoring: CloudWatch + CloudTrail")
