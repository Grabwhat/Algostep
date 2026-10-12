# AlgoStep ⚡</>

**Build your problem-solving skills, one step at a time.**

AlgoStep is a competitive programming learning platform designed to help students develop their problem-solving and algorithmic thinking skills through structured practice, progressive difficulty levels, and guided learning resources.

Instead of jumping straight into difficult problems, learners can build their foundations, practice specific topics, and track their progress as they improve.

## Features

- **Structured Learning Path**: Explore competitive programming topics in an organized progression.
- **Curated Problems**:         Practice problems organized by topic and difficulty.
- **Guided Hints**:             Get help approaching a problem without immediately revealing the solution.
- **Editorials**:               Review explanations and understand the reasoning behind problem-solving approaches.
- **Progress Tracking**:        Keep track of your learning progress as you solve problems.
- **XP and Level Progression**: Earn experience points and work toward higher levels as you practice.
- **User Profiles**:            Maintain a profile to personalize your learning experience.

## Snippets of Algostep

<img width="1890" height="812" alt="image" src="https://github.com/user-attachments/assets/78e9acd0-811d-427c-bca6-3dff864e9476" />
<img width="1891" height="972" alt="image" src="https://github.com/user-attachments/assets/bc21f592-3bf4-43c0-b304-0b97ef6c789d" />
<img width="1905" height="847" alt="image" src="https://github.com/user-attachments/assets/24b080ad-4e61-4d3e-9d8a-806b33ad890c" />
<img width="1887" height="882" alt="image" src="https://github.com/user-attachments/assets/8b811113-b39d-446c-a3a5-0e83c0b50836" />
<img width="1878" height="877" alt="image" src="https://github.com/user-attachments/assets/cf5d6713-7512-44ea-a8c3-5dda0f680a1d" />



## Topics

AlgoStep's curriculum focuses on foundational competitive programming techniques, including:

- Arrays and Hashing
- Two Pointers
- Stack
- Complete Search
- Simulation
- Sliding Window
- Binary Search

The goal is to help learners build a strong foundation before progressing to more advanced algorithms and data structures in a gamified fashion.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Tailwind CSS
- **Syntax Highlighting:** Prism.js
- **Database:** Handled by Django's Object-Relational Mapper (ORM)
- **Frontend Tooling:** Node.js and npm

## Getting Started

Follow these steps to run AlgoStep locally:

### Prerequisites

Install the following before getting started:

- Python 3
- Node.js and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Grabwhat/Algostep.git
```

Replace the placeholders with your actual GitHub repository URL and directory name.

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows (Command Prompt):**

```bat
.venv\Scripts\activate
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root, alongside `manage.py` (which is already created for you).

Add the variables required by your Django settings. For example:

```dotenv
DJANGO_SECRET_KEY=your-local-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Generate your own local secret key and keep `.env` private. **Never commit `.env` or real secret keys to GitHub.**

See `.env.example` for the required variable names and expected configuration.

### 5. Install Frontend Dependencies

Install the Node.js dependencies from the project root:

```bash
npm install
```

### 6. Build Tailwind CSS

AlgoStep uses Tailwind CSS to style its interface.

**For development:** Start the Tailwind watcher to automatically rebuild the CSS when changes are detected.

```bash
npm run dev
```

Keep this terminal running while developing.

**For production:** Generate a minified CSS file.

```bash
npm run build
```

Both commands compile `static/src/input.css` into `static/dist/output.css`.

Make sure the generated CSS file exists before running the Django development server, since the website uses it for styling.

Check `package.json` for the actual script name used by this project.

### 7. Set Up the Database

Apply Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Load Algostep's curriculum data (contains every problem and topic):

```bash
python manage.py loaddata algostep_content.json
```

### 8. Create an Administrator Account (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your local administrator account.

### 9. Run the Development Server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project Structure

The exact structure may vary as the project evolves.
Note: for the 'apps' directory, this is for all the apps you've made (one folder for each app), not just one folder for all of them. 

```text
Algostep/
├── manage.py
├── requirements.txt
├── package.json
├── package-lock.json
├── .env.example
├── .gitignore
├── algostep/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── apps/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
|
└── static/
    ├── css/
    ├── js/
    ├── src/
    │   └── input.css
    └── dist/
        └── output.css
```

## Security

- Never commit `.env`, production credentials, or secret keys.
- Do not commit private user data or your local development database.
- Keep production settings separate from local development settings.
- Use `DEBUG=False`, appropriate allowed hosts, HTTPS, and secure settings when deploying.

## Future Improvements

- Expanding the problem library and learning curriculum.
- Adding more algorithm and data structure topics.
- Improving personalized learning progression.
- Adding more detailed progress insights and learning resources.
- Using HTMX for cleaner UX
- A browser IDE using Monaco Editor, WebAssembly (WASM), and a Docker container


## License 

No license has been specified yet. Unless a license is added, others generally do not receive permission to reuse, distribute, or modify this code just because the repository is public.
---
