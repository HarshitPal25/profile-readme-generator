"""
GitHub Profile README Generator (Interactive CLI)

Run: python github_profile_readme_generator.py

Optional dependencies (recommended for prettier terminal UI):
    pip install rich

What it does:
- Asks interactive questions (name, bio, skills, projects, socials, theme)
- Lets you pick an ASCII avatar (or provide your own)
- Generates a polished README.md using badges, sections, and GitHub stats/metrics links
- Optionally previews the README in terminal and writes README.md in current folder

Author: Generated for you by ChatGPT
"""

from datetime import datetime
import textwrap
import webbrowser
import os
import sys

try:
    from rich import print
    from rich.prompt import Prompt, Confirm
    from rich.console import Console
    from rich.table import Table
except Exception:
    # Fallback to basic input/print if rich is not installed
    def print(*args, **kwargs):
        __builtins__.print(*args, **kwargs)
    def Prompt():
        raise RuntimeError("Rich is optional but recommended. Run: pip install rich")
    class SimplePrompt:
        @staticmethod
        def ask(msg, default=None):
            val = input(f"{msg} ")
            return val or default
    class SimpleConfirm:
        @staticmethod
        def ask(msg, default=False):
            val = input(f"{msg} (y/n) ")
            return val.lower().startswith('y')
    Console = None
    Prompt = SimplePrompt
    Confirm = SimpleConfirm

console = Console() if 'Console' in globals() and Console else None

ASCII_AVATARS = {
    "Coder": r"""
      .--.
     |o_o |
     |:_/ |
    //   \\
   (|     | )
  /'\_   _/`\\
  \___)=(___/
""",
    "Robot": r"""
     [=]   [=]
      |-----|
     /|     |\\
    /_|_____|_\\
      /_/ \_\\
    """,
    "Minimal": r"""
     (^_^)
    """,
}

BADGE_TMPL = "https://img.shields.io/badge/{label}-{message}-{color}.svg?style=for-the-badge&logo={logo}"

def ask(prompt_text, default=None):
    try:
        return Prompt.ask(prompt_text, default=default)
    except Exception:
        val = input(f"{prompt_text} ")
        return val if val.strip() else default

def confirm(prompt_text, default=False):
    try:
        return Confirm.ask(prompt_text, default=default)
    except Exception:
        val = input(f"{prompt_text} (y/n) ")
        return val.lower().startswith('y')

def choose_avatar():
    print("\nChoose an avatar (or press Enter to skip):")
    keys = list(ASCII_AVATARS.keys())
    for i, k in enumerate(keys, 1):
        print(f"  {i}. {k}")
    choice = ask("Enter number of avatar", default="1")
    try:
        i = int(choice) - 1
        return ASCII_AVATARS[keys[i]]
    except Exception:
        return ""

def make_badge(label, message, color='4c1', logo='github'):
    # Safe-encode label & message minimally
    from urllib.parse import quote_plus
    return BADGE_TMPL.format(label=quote_plus(label), message=quote_plus(message), color=color, logo=quote_plus(logo))

READMETPL = '''# {name} {emoji}

{avatar}

[![Visitors](https://visitor-badge.laobi.icu/badge?page_id={github_username})]

{shortbio}

{badges}

---

## 🔭 I'm currently
{currently}

## 🌱 I’m learning
{learning}

## 👯 I’m looking to collaborate on
{collab}

## 💬 Ask me about
{about}

## 📫 How to reach me
{contacts}

## ⚡ Fun fact
{fun}

---

### 🛠️ Skills & Tools
{skills}

---

### 📂 Projects
{projects}

---

Last updated: {date}
'''

PROJECT_ITEM = '- [{title}]({link}) — {desc}'

def build_markdown(data):
    badges = []
    # Language badges
    for lang in data['top_langs']:
        badges.append(f"![{lang}]({make_badge(lang, 'proficient', 'blue', 'code')})")
    # social badges
    if data.get('linkedin'):
        badges.append(f"[![LinkedIn]({make_badge('LinkedIn', data['linkedin'], '0e76a8', 'linkedin')})]({data['linkedin']})")
    if data.get('twitter'):
        badges.append(f"[![Twitter]({make_badge('Twitter', data['twitter'].lstrip('@'), '1DA1F2', 'twitter')})](https://twitter.com/{data['twitter'].lstrip('@')})")
    if data.get('website'):
        badges.append(f"[![Website]({make_badge('Website', 'portfolio', 'ff69b4', 'google-chrome')})]({data['website']})")

    badge_str = ' '.join(badges)

    skills_md = '\n'.join([f'- {s}' for s in data['skills']]) if data['skills'] else '- Not listed yet'

    projects_md = '\n'.join([PROJECT_ITEM.format(title=p['name'], link=p['link'], desc=p['desc']) for p in data['projects']]) if data['projects'] else '- No projects listed yet'

    contacts = []
    if data.get('email'):
        contacts.append(f"Email: [{data['email']}](mailto:{data['email']})")
    if data.get('github_username'):
        contacts.append(f"GitHub: [{data['github_username']}](https://github.com/{data['github_username']})")
    if data.get('linkedin'):
        contacts.append(f"LinkedIn: {data['linkedin']}")

    contacts_md = '  \n'.join(contacts) if contacts else 'Not provided'

    avatar = '```\n' + data.get('avatar','') + '\n```' if data.get('avatar') else ''

    return READMETPL.format(
        name=data['name'],
        emoji=data.get('emoji',''),
        avatar=avatar,
        github_username=data.get('github_username','username'),
        shortbio=data.get('short_bio','A passionate developer.'),
        badges=badge_str,
        currently=data.get('currently','Working on cool stuff.'),
        learning=data.get('learning','New technologies.'),
        collab=data.get('collab','Open to collaboration.'),
        about=data.get('about','Software, systems, design.'),
        contacts=contacts_md,
        fun=data.get('fun','Coffee enthusiast ☕'),
        skills=skills_md,
        projects=projects_md,
        date=datetime.utcnow().strftime('%Y-%m-%d')
    )


def main():
    print('\n[bold underline]GitHub Profile README Generator[/]\n')
    data = {}
    data['name'] = ask('Your full name', default=os.getlogin() if hasattr(os, 'getlogin') else 'Your Name')
    data['github_username'] = ask('GitHub username (for visitor counter and links)', default='your-github')
    data['emoji'] = ask('Pick an emoji to show after your name (e.g. 😄, 🚀)', default='🚀')
    use_avatar = confirm('Would you like to add a small ASCII avatar?', default=True)
    data['avatar'] = choose_avatar() if use_avatar else ''
    data['short_bio'] = ask('Short bio / one-liner', default='Passionate about building things and learning new tech.')
    data['currently'] = ask('What are you currently working on?', default='Open-source projects and learning.')
    data['learning'] = ask('What are you learning?', default='Deepening knowledge in backend and infra.')
    data['collab'] = ask('What would you like to collaborate on?', default='Open to backend and automation projects.')
    data['about'] = ask('What topics can people ask you about?', default='Python, DevOps, Security')
    data['email'] = ask('Email (optional)', default='')
    data['linkedin'] = ask('LinkedIn URL (optional)', default='')
    data['twitter'] = ask('Twitter handle (optional, without @)', default='')
    data['website'] = ask('Personal website or portfolio (optional)', default='')
    data['fun'] = ask('A fun fact about you', default='I love coffee and chess.')

    langs = ask('Top 3 languages/tech (comma separated, e.g. Python,Go,React)', default='Python,JavaScript')
    data['top_langs'] = [l.strip() for l in langs.split(',') if l.strip()][:5]

    skills = ask('List your main skills (comma separated)', default='Python,APIs,Automation')
    data['skills'] = [s.strip() for s in skills.split(',') if s.strip()]

    # Projects input
    projects = []
    if confirm('Add projects now?', default=True):
        while True:
            name = ask('Project name (empty to stop)', default='')
            if not name:
                break
            link = ask('Project link (repo or demo)', default='#')
            desc = ask('One-line description', default='One-liner about the project')
            projects.append({'name': name, 'link': link, 'desc': desc})
            if not confirm('Add another project?', default=True):
                break
    data['projects'] = projects

    md = build_markdown(data)

    print('\n[bold]Preview of generated README:[/]\n')
    print(md)

    if confirm('Write README.md to current directory?', default=True):
        path = os.path.join(os.getcwd(), 'README.md')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"\n✅ README.md written to: {path}")
        if confirm('Open README.md in default app?', default=False):
            try:
                webbrowser.open(f'file://{path}')
            except Exception:
                print('Could not open automatically — please open it manually.')
    else:
        print('Aborted — README.md not written.')

    print('\nDone! You can copy, tweak, and push README.md to your GitHub profile repo (username/username).')

if __name__ == '__main__':
    main()
