# AI Support Copilot with RAG, MySQL, FastAPI, and Streamlit

## 1. Project Overview

AI Support Copilot is an end-to-end portfolio project that demonstrates how artificial intelligence, retrieval-augmented generation, SQL analytics, and API development can be combined to support customer service teams.

The project uses customer support ticket data, stores cleaned ticket records in MySQL, retrieves relevant support knowledge using a Chroma vector database, and generates suggested support replies through a RAG-based workflow. It also includes a FastAPI backend and a Streamlit demo app for interactive use.

This project is designed to demonstrate practical skills in:

* Python data engineering
* SQL database loading and querying
* Machine learning baseline modeling
* RAG-based knowledge retrieval
* FastAPI backend development
* Streamlit application development
* AI support workflow automation

---

## 2. Business Problem

Customer support teams often receive a high volume of repetitive tickets related to billing, refunds, cancellations, product issues, technical problems, and escalations.

Common challenges include:

* Slow first response times
* Inconsistent support replies
* Difficulty finding the right policy or troubleshooting guide
* Manual ticket review
* Repetitive agent workload
* Lack of structured ticket analytics
* Difficulty identifying escalation-worthy issues

A support copilot can help agents respond faster, stay consistent with internal policies, and improve support quality.

---

## 3. Solution

This project builds an AI-assisted support workflow that:

1. Loads and cleans customer support ticket data.
2. Stores structured tickets in a MySQL database.
3. Creates a support knowledge base using markdown policy and FAQ documents.
4. Converts knowledge base content into embeddings using SentenceTransformers.
5. Stores embeddings in ChromaDB for semantic retrieval.
6. Retrieves relevant knowledge base sections for a given ticket.
7. Generates a suggested support reply using retrieved context.
8. Exposes the workflow through FastAPI endpoints.
9. Provides a Streamlit demo app for ticket selection and reply generation.

The project combines structured ticket data from MySQL with unstructured knowledge base retrieval from ChromaDB.

---

## 4. Key Features

### Data Pipeline

* Loads customer support ticket data from CSV.
* Cleans text, categorical, numeric, and time-related fields.
* Preserves missing-value indicators for analytics.
* Saves cleaned data for downstream use.

### MySQL Ticket Storage

* Creates a MySQL database and support ticket table.
* Loads cleaned support ticket records into MySQL.
* Supports ticket lookup by ticket ID.
* Supports recent ticket retrieval for demos and API use.

### SQL Analytics

* Ticket volume by type, priority, status, and channel.
* Average satisfaction by ticket type and channel.
* Missing resolution analysis.
* Product-level ticket volume.
* Dashboard-ready SQL views.

### Machine Learning Baseline

* TF-IDF based supervised ticket classification.
* Logistic Regression and Random Forest baseline models.
* Accuracy and cross-validation evaluation.
* Data quality review of noisy labels.

### RAG Knowledge Retrieval

* Markdown-based support knowledge base.
* ChromaDB vector store.
* SentenceTransformer embeddings using `all-MiniLM-L6-v2`.
* Semantic retrieval of relevant support documents.
* Source-aware retrieval output.

### Suggested Reply Generation

* Template-based RAG response generation.
* Uses retrieved context from the knowledge base.
* Uses enriched ticket metadata such as priority, status, channel, and product.
* Generates support replies for billing, cancellation, login, product compatibility, hardware, and escalation scenarios.

### FastAPI Backend

* Health check endpoint.
* Retrieve relevant knowledge base context.
* Generate suggested replies from text.
* Fetch tickets from MySQL.
* Generate suggested replies for stored MySQL tickets.

### Streamlit Demo App

* Displays recent tickets from MySQL.
* Allows selecting a ticket.
* Shows ticket metadata and customer message.
* Generates RAG-based suggested replies.
* Displays retrieved knowledge base sources.
* Shows full API response for transparency.

---

## 5. Tech Stack

| Area                 | Tools / Libraries          |
| -------------------- | -------------------------- |
| Programming Language | Python                     |
| Data Processing      | Pandas                     |
| Machine Learning     | Scikit-learn               |
| Embeddings           | SentenceTransformers       |
| Vector Database      | ChromaDB                   |
| Database             | MySQL                      |
| Database Access      | SQLAlchemy, PyMySQL        |
| API Backend          | FastAPI, Uvicorn, Pydantic |
| Frontend Demo        | Streamlit                  |
| API Requests         | Requests                   |
| Model Persistence    | Joblib                     |
| Development          | VS Code, Git, GitHub       |

Note: The current version uses a template-based RAG response generator. It can be extended later with OpenAI, Azure OpenAI, or another LLM provider.

---

## 6. Project Architecture

```text
Customer Support Ticket Dataset
        ↓
Data Cleaning Notebook
        ↓
Cleaned CSV
        ↓
Python ETL Loader
        ↓
MySQL support_tickets table
        ↓
FastAPI Ticket Repository
        ↓
Ticket Lookup API
        ↓
RAG Reply Endpoint
        ↓
Streamlit Demo App
```

```text
Knowledge Base Markdown Files
        ↓
Text Chunking
        ↓
SentenceTransformer Embeddings
        ↓
ChromaDB Vector Store
        ↓
Semantic Retrieval
        ↓
RAG Context
        ↓
Suggested Support Reply
```

Full workflow:

```text
MySQL Ticket Data + Chroma Knowledge Base
        ↓
FastAPI Backend
        ↓
RAG Retrieval and Reply Generator
        ↓
Streamlit Support Copilot Interface
```

---

## 7. Dataset

This project uses the Kaggle Customer Support Ticket Dataset.

The dataset includes support ticket fields such as:

* Ticket ID
* Customer demographic fields
* Product purchased
* Ticket type
* Ticket subject
* Ticket description
* Ticket status
* Ticket priority
* Ticket channel
* First response time
* Time to resolution
* Customer satisfaction rating
* Resolution text

The full raw dataset is not committed to the repository. Only sample or processed outputs should be included where appropriate, depending on dataset licensing and repository size considerations.

---

## 8. Repository Structure

```text
ai-support-copilot-rag/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_ticket_classification_model.ipynb
│   └── 03_rag_experiment.ipynb
├── src/
│   ├── data/
│   │   ├── clean_data.py
│   │   ├── db_loader.py
│   │   └── ticket_repository.py
│   ├── models/
│   │   ├── predict_category.py
│   │   └── train_classifier.py
│   ├── rag/
│   │   ├── build_vector_store.py
│   │   ├── retrieve_docs.py
│   │   └── generate_answer.py
│   ├── api/
│   │   └── main.py
│   └── utils/
│       └── config.py
├── app/
│   └── streamlit_app.py
├── sql/
│   ├── create_tables.sql
│   ├── sample_queries.sql
│   └── views.sql
├── knowledge_base/
│   ├── billing_faq.md
│   ├── refund_policy.md
│   ├── cancellation_policy.md
│   ├── technical_troubleshooting.md
│   ├── product_information.md
│   └── escalation_policy.md
├── docs/
├── models/
├── vector_store/
└── tests/
```

---

## 9. How to Run Locally

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd ai-support-copilot-rag
```

### Step 2: Create and Activate Virtual Environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file using `.env.example` as a reference.

Example for local XAMPP MySQL:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=support_copilot_db
```

### Step 5: Start MySQL

Start MySQL using XAMPP or your preferred local MySQL setup.

Create the database and table using:

```sql
sql/create_tables.sql
```

### Step 6: Load Data into MySQL

After preparing the cleaned dataset, run:

```bash
python -m src.data.db_loader
```

### Step 7: Build Chroma Vector Store

The vector store is generated locally and should not be committed to GitHub.

```bash
python -B -u -m src.rag.build_vector_store
```

### Step 8: Test RAG Retrieval

```bash
python -B -u -m src.rag.retrieve_docs
```

### Step 9: Test Suggested Reply Generation

```bash
python -B -u -m src.rag.generate_answer
```

### Step 10: Run FastAPI Backend

```bash
python -B -m uvicorn src.api.main:app --reload
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

### Step 11: Run Streamlit Demo App

Open a second terminal, activate the virtual environment, then run:

```bash
streamlit run app/streamlit_app.py
```

Open the Streamlit app:

```text
http://localhost:8501
```

---

## 10. API Endpoints

### Root

```http
GET /
```

Returns a basic API status message and available endpoints.

### Health Check

```http
GET /health
```

Returns API health status.

### Retrieve Knowledge Base Context

```http
POST /retrieve
```

Example request:

```json
{
  "ticket_text": "I was charged twice for my order and need help with the payment.",
  "top_k": 3
}
```

Returns relevant knowledge base chunks from ChromaDB.

### Generate Suggested Reply from Text

```http
POST /suggest-reply
```

Example request:

```json
{
  "ticket_text": "I cannot login to my account after resetting my password.",
  "top_k": 3
}
```

Returns a suggested support reply based on RAG context.

### Get Recent Tickets

```http
GET /tickets/recent
```

Optional query parameter:

```text
limit=10
```

Returns recent support tickets from MySQL.

### Get Ticket by ID

```http
GET /tickets/{ticket_id}
```

Returns a single support ticket from MySQL.

### Generate Suggested Reply for a Stored Ticket

```http
POST /tickets/{ticket_id}/suggest-reply
```

Optional query parameter:

```text
top_k=3
```

This endpoint:

1. Fetches a ticket from MySQL.
2. Cleans placeholder values such as `{product_purchased}`.
3. Enriches the ticket text with metadata.
4. Retrieves relevant knowledge base context from ChromaDB.
5. Generates a suggested support reply.

---

## 11. Example Output

For a ticket involving a Dyson Vacuum Cleaner making unusual noises and not functioning correctly, the system generates a response such as:

```text
Thank you for contacting support. I’m sorry to hear that your Dyson Vacuum Cleaner is making unusual noises and is not functioning properly.

To help us investigate this further, please confirm the exact product model, when the issue first started, whether the noise happens continuously or only at certain times, and whether any error message or warning indicator appears. Please also let us know if you have already tried restarting or resetting the product.

Because this may involve a hardware-related issue, we may need to escalate the case to our technical support team after reviewing these details. Screenshots, short videos, or any additional evidence of the issue would also help us diagnose the problem more quickly.
```

The system also returns sources used, such as:

```text
technical_troubleshooting.md
escalation_policy.md
billing_faq.md
```

---

## 12. Machine Learning Baseline

A supervised ticket classification baseline was trained using TF-IDF features and classification models.

Models tested:

* TF-IDF + Logistic Regression
* TF-IDF + Random Forest

The best baseline model achieved approximately 21% accuracy, which is close to the expected random baseline for a five-class classification problem.

Manual label review showed that some dataset labels were inconsistent with the actual ticket text. For example, some tickets labeled as billing, refund, or cancellation appeared to describe technical issues.

Because of this data quality issue, the classifier is retained as a baseline experiment rather than a production-quality model.

The main production focus of this project is:

* RAG-based support assistance
* SQL analytics
* Ticket retrieval from MySQL
* API-based support automation
* Streamlit-based demo interface

---

## 13. SQL Analytics

The project includes SQL scripts for analytics and reporting.

Example analytics:

* Total tickets
* Ticket count by type
* Ticket count by priority
* Ticket count by status
* Ticket count by channel
* Average satisfaction by ticket type
* Average satisfaction by support channel
* Missing resolution analysis
* Product-level ticket volume

SQL views are included to support dashboarding and reporting use cases.

---

## 14. Streamlit Demo App

The Streamlit app provides a user-friendly interface for the support copilot.

Features:

* View recent support tickets from MySQL.
* Select a ticket from the table.
* View ticket metadata and customer message.
* Generate a RAG-based suggested reply.
* View knowledge base sources used.
* Inspect retrieved context chunks.
* View full API response.

This makes the project easier to demonstrate to recruiters, hiring managers, and technical reviewers.

---

## 15. Screenshots

Suggested screenshots to add:

```text
screenshots/
├── streamlit_ticket_list.png
├── streamlit_generated_reply.png
├── swagger_api_docs.png
├── mysql_ticket_table.png
└── rag_retrieved_context.png
```

Add screenshots after running the app locally.

---

## 16. Business Impact

This project demonstrates how AI can support customer service operations by:

* Reducing time spent drafting repetitive replies.
* Improving consistency across agents.
* Helping agents find relevant policy and troubleshooting content.
* Supporting faster escalation decisions.
* Improving first-response quality.
* Enabling structured analytics from ticket history.
* Creating a foundation for human-in-the-loop support automation.

The system is not designed to replace support agents. It is designed to assist agents by generating draft replies and surfacing relevant knowledge base context.

---

## 17. Limitations

Current limitations include:

* The response generator is template-based, not powered by a live LLM.
* The dataset appears to contain noisy or inconsistent labels.
* The knowledge base is manually created for demonstration purposes.
* The vector store is local and must be rebuilt after cloning.
* No authentication is currently implemented for the API.
* No human feedback loop is currently implemented.
* The classifier is not suitable for production use without better labels.

---

## 18. Future Improvements

Planned improvements include:

* Add OpenAI or Azure OpenAI for more natural response generation.
* Add human approval workflow before sending replies.
* Add feedback capture for generated replies.
* Add CRM or helpdesk integration.
* Add authentication and user roles.
* Add Docker support for easier deployment.
* Add automated tests.
* Add monitoring and logging.
* Add multilingual support, including Arabic.
* Improve classification using better-labeled data.
* Add escalation scoring.
* Add response quality evaluation.
* Add MLOps pipeline for retraining and evaluation.

---

## 19. Skills Demonstrated

This project demonstrates practical experience in:

* Python application development
* Data cleaning and preprocessing
* Exploratory data analysis
* SQL database design
* MySQL integration
* SQLAlchemy usage
* Machine learning baseline modeling
* TF-IDF feature extraction
* Model evaluation and data quality diagnosis
* Embedding generation
* Vector database creation
* ChromaDB semantic search
* Retrieval-Augmented Generation workflow
* FastAPI backend development
* Pydantic validation
* Streamlit app development
* API integration
* Git and GitHub project organization

---

## 20. Author

**Muhammad Usman Dilshad**

Technology Specialist | Data, AI, Automation, and Software Engineering Portfolio
https://www.linkedin.com/in/customer-success-saas-data-scientist-ai-agents-machine-learning/