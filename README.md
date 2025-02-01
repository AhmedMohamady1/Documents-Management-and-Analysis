# Document Management and Analysis Tool

## Overview
This project is a **Python-based text analysis tool** leveraging **MongoDB** for efficient document storage and retrieval. It allows users to upload, manage, and analyze text-based documents through powerful query capabilities, including metadata extraction, term frequency analysis, and similarity calculations.

---

## Key Features
- **Document Management:** Upload, store, and delete text documents (PDF, DOCX, TXT).
- **Metadata Extraction:** Extract essential document metadata, such as number of pages, file type, and modification date.
- **Regex-Powered Queries:** Construct and execute complex queries using regular expressions.
- **Search Functionality:** Locate specific document contents or metadata.
- **Common Word Identification:** Find the most frequently occurring words across documents.
- **Term Frequency Analysis:** Calculate the frequency of terms or phrases within documents.
- **Similarity Analysis:** Compare two documents using distance measures (Cosine Similarity, Jaccard Similarity).
- **Dissimilarity Calculation:** Compute the Euclidean distance between two document representations.

---

## Technical Components
- **Programming Language:** Python
- **Database:** MongoDB (for document storage and management)
- **Libraries:**
  - `re`: Regular expression operations for pattern matching
  - `math`: Mathematical functions for similarity and dissimilarity metrics
- **User Interface:** Command-line interface (CLI)

---

## Project Workflow
1. **Document Input:** Users upload text-based documents.
2. **Metadata Extraction:** Automatic extraction and storage of metadata.
3. **Data Storage:** Both document content and metadata are stored in MongoDB.
4. **Query Interface:** Users interact via CLI to execute queries.
5. **Result Processing:** Relevant query results are retrieved and displayed.

---

## Usage Instructions
1. **Upload Documents:** Follow CLI prompts to upload documents.
2. **Execute Queries:** Use the CLI to perform regex-based queries, frequency analysis, and similarity checks.
3. **View Results:** Analyze the displayed results based on your query needs.

---

## Potential Applications
- **Academic Research:** Analyze research papers, identify patterns, and compare textual content.
- **Corporate Document Management:** Manage and analyze reports and documents.
- **Legal Analysis:** Compare contracts and extract key clauses.
- **Market Review Analysis:** Analyze customer reviews and product descriptions.

---

## Future Improvements
- Web-based graphical user interface (GUI)
- Enhanced NLP features (sentiment analysis, named entity recognition)
- Cloud database integration for scalable deployments

---
