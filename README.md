![DocumentLM GitHub Banner](https://documentlm.s3.ap-south-1.amazonaws.com/images/github-banner.png)

<div align="center">
   <div>
      <h3>
        <a href="https://langfuse.com/blog/2025-06-04-open-sourcing-langfuse-product">
            <strong>Rhobots Is Doubling Down On Open Source</strong>
         </a> <br> <br>
         <a href="https://documentlm.rhobots.ai">
            <strong>DocumentLM Cloud</strong>
         </a> ·
        <strong>Self Host</strong>
      </h3>
   </div>

   <span>DocumentLM uses <a href="https://github.com/orgs/rhobots-ai/discussions"><strong>Github Discussions</strong></a>  for Support and Feature Requests.</span>
   <br/>
   <br/>
   <div>
   </div>
</div>

<p align="center">
   <a href="https://github.com/rhobots-ai/documentlm/blob/main/LICENSE">
   <img src="https://img.shields.io/badge/License-MIT-E11311.svg" alt="MIT License">
   </a>
</p>

DocumentLM is an **open source AI Research** platform.
From Text to Video—One AI for All Your Research.
It helps you analyze **unstructured data**, extract insights, and collaborate in one powerful workspace. DocumentLM can be **self-hosted in minutes**.

## 📦 Deploy DocumentLM

### DocumentLM Cloud

Managed deployment by the DocumentLM team, generous free-tier, no credit card required.

<div align="center">
    <a href="https://documentlm.rhobots.ai" target="_blank">
        Sign Up for DocumentLM
    </a>
</div>

### Self-Host DocumentLM

Run DocumentLM on your own machine in 5 minutes using Docker Compose.

  ```bash
  # Get a copy of the latest Langfuse repository
  git clone https://github.com/rhobots-ai/documentlm.git
  cd documentlm
  
  # Copy .env.example to .env
  cp .env.example .env
  
  # Ensure to add your OPENAI_API_KEY
  vim .env

  # Run the DocumentLM docker compose
  docker compose up
  ```
To create a user, you can sign up via email or you can run the below script.

 ```bash
 ./scripts/init-db-user.sh
 ```

## ⭐️ Star Us

![star-documentlm-on-github](https://documentlm.s3.ap-south-1.amazonaws.com/images/github-star.gif)

## 🥇 License

This repository is MIT licensed, except for the `ee` folders. See [LICENSE](LICENSE).
