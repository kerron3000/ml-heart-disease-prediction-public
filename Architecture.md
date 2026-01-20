flowchart LR
    Dev[Developer]
    GitHub[GitHub Repository]

    subgraph CI_CD[CI/CD & Security]
        Gitleaks[Gitleaks<br/>Secrets Detection]
        Bandit[Bandit<br/>SAST]
        Semgrep[Semgrep<br/>SAST]
        TrivySCA[Trivy<br/>SCA]
    end

    subgraph IaC[Infrastructure as Code]
        Terraform[Terraform]
    end

    subgraph AWS[AWS Cloud]
        ECR[ECR<br/>Docker Registry]
        
        subgraph ECS[ECS Fargate Cluster]
            Task[ML Inference Container<br/>Streamlit App]
        end
    end

    User[End User<br/>Browser]

    Dev --> GitHub
    GitHub --> Gitleaks
    GitHub --> Bandit
    GitHub --> Semgrep
    GitHub --> TrivySCA

    GitHub --> Terraform
    Terraform --> ECR
    Terraform --> ECS

    GitHub -->|Docker Build| ECR
    ECR --> ECS

    User -->|HTTP| ECS
