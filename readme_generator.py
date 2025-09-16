def generate_readme():
    print("🚀 GitHub Profile README Generator\n")

    name = input("Enter your name: ")
    bio = input("Enter a short bio/description: ")
    skills = input("Enter your skills (comma separated): ")
    github_username = input("Enter your GitHub username: ")
    linkedin = input("Enter your LinkedIn URL: ")
    twitter = input("Enter your Twitter URL: ")

    readme = f"""# Hi there 👋, I'm {name}

## 🚀 About Me
{bio}

## 🛠️ Skills
{', '.join(skill.strip() for skill in skills.split(','))}

## 📊 GitHub Stats
![GitHub Stats](https://github-readme-stats.vercel.app/api?username={github_username}&show_icons=true&theme=radical)

## 🌐 Connect with me
- [LinkedIn]({linkedin})
- [Twitter]({twitter})
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("\n✅ README.md has been generated!")


if __name__ == "__main__":
    generate_readme()
