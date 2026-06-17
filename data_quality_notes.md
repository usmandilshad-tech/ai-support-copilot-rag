# Data Quality Notes

## Dataset

This project uses the Kaggle Customer Support Ticket Dataset for demonstration purposes.

## Label Quality Review

During exploratory modeling, a baseline supervised classifier was trained to predict `ticket_type` using the combined ticket subject and description.

The best baseline model achieved approximately 21% accuracy, which is close to the expected random baseline of 20% for a five-class classification problem.

Manual review of sampled records showed that some ticket labels appear inconsistent with the ticket text. For example:

- Some records labeled as `Billing inquiry` appear to describe technical issues.
- Some records labeled as `Cancellation request` appear to describe technical issues.
- Some records labeled as `Refund request` appear to describe technical issues.

## Impact

Because supervised machine learning depends on reliable labels, the `ticket_type` field is not suitable for building a high-quality production classifier without relabeling or using a better-labeled dataset.

## Project Decision

The classifier is retained as a baseline experiment to demonstrate the modeling workflow, evaluation process, and data-quality diagnosis.

The main project focus is shifted toward:

- RAG-based support response generation
- SQL analytics
- Support dashboarding
- AI-assisted ticket triage
- Workflow automation
- API-based support copilot integration

This reflects a realistic AI project workflow where data quality findings influence solution design.