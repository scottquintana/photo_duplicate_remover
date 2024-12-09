# Photo Duplicate Remover

**A basic script to search a drive for duplicate photos and move only one copy to a folder.**

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Installation](#installation)  
3. [Running the Project](#running-the-project)  
4. [Virtual Environment](#virtual-environment)  
5. [Project Structure](#project-structure)  
6. [Contributing](#contributing)  

---

## Project Overview

This project is a Python application that scans for duplicate photo/video files.

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/scottquintana/photo_duplicate_remover.git
    cd photo_duplicate_remover
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate    # On macOS or Linux
    .\.venv\Scripts\activate     # On Windows
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

To run the project:

```bash
python find_duplicates.py
```

## Virtual Environment

The project uses a virtual environment to manage dependencies. The virtual environment is excluded from version control using `.gitignore`.

### Activating the Virtual Environment

- **macOS / Linux**:

  ```bash
  source .venv/bin/activate
  ```

- **Windows**:

  ```bash
  .\.venv\Scripts\activate
  ```

### Deactivating the Virtual Environment

To deactivate the virtual environment:

```bash
deactivate
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Submit a pull request.
