def generate_readme():
    name = input("Enter you name: ")
    bio = input("Enter you bio/short discription: ")
    skills = input("Enter your skills(Comma seperated): ")
    github_username= input("Enter your github username: ")
    linkdin = input("Enter you linkdin URL: ")

    readme = f"""
# Hi There 👋, I am {name}
[![Visitors](https://visitor-badge.laobi.icu/badge?page_id={github_username})]
## 🚀 About Me
{bio}
## 🛠️ Skills
{", ".join(skill.strip() for skill in skills.split(","))}
## 📊 GitHub Stats
![GitHub Stats](https://github-readme-stats.vercel.app/api?username={github_username}&show_icons=true&theme=radical)
## 🌐 Connect with me
[LinkdIn]({linkdin})
        """
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("README.md generated successfully!")

if __name__ == "__main__" :
    generate_readme()





    