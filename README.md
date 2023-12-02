# CBSE Question Papers Downloader

## Overview

This Python script allows you to download CBSE question papers for a specific subject and standard (class).

## Prerequisites

- Python 3.x
- pip

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/00lohit/CBSE_question_papers.git
    cd cbse-question-papers
    ```

2. Run the setup script to create and activate the virtual environment:

    ```bash
    source setup.sh
    ```

    On Windows, use:

    ```bash
    .\setup.sh
    ```

    This script sets up a virtual environment and installs the required dependencies.

## Usage

1. Modify the `subject_name` and `standard` variables in the `download_question_papers` function inside `main.py`:

    ```python
    subject_name = 'ACCOUNTANCY'
    standard = 'XII'
    ```

2. Run the script to download question papers:

    ```bash
    python main.py
    ```

    The downloaded question papers will be saved in the `question_papers` folder.

## Deactivation

To deactivate the virtual environment:

```bash
deactivate
