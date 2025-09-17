import os

parent_dir=".github"
sub_dir="workflows"
os.mkdir(parent_dir)
path = os.path.join(parent_dir,sub_dir)
os.mkdir(path)

path_to_sub_dir = ".github/workflows"
file_name= "snake.yml"
file_path =os.path.join(path_to_sub_dir,file_name)

with open(file_path,"w") as f:
    f.write("""name: GitHub Snake Game



on:

  # Schedule the workflow to run daily at midnight UTC

  schedule:

    - cron: "0 0 * * *"



  # Allow manual triggering of the workflow

  workflow_dispatch:



  # Trigger the workflow on pushes to the main branch

  push:

    branches:

      - main



jobs:

  generate:

    runs-on: ubuntu-latest

    timeout-minutes: 10



    steps:

      # Step 1: Checkout the repository

      - name: Checkout Repository

        uses: actions/checkout@v3



      # Step 2: Generate the snake animations

      - name: Generate GitHub Contributions Snake Animations

        uses: Platane/snk@v3

        with:

          # GitHub username to generate the animation for

          github_user_name: ${{ github.repository_owner }}



          # Define the output files and their configurations

          outputs: |

            dist/github-snake.svg

            dist/github-snake-dark.svg?palette=github-dark

            dist/ocean.gif?color_snake=orange&color_dots=#bfd6f6,#8dbdff,#64a1f4,#4b91f1,#3c7dd9

        env:

          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}



      # Step 3: Deploy the generated files to the 'output' branch

      - name: Deploy to Output Branch

        uses: peaceiris/actions-gh-pages@v3

        with:

          github_token: ${{ secrets.GITHUB_TOKEN }}

          publish_dir: ./dist

          publish_branch: output

          # Optionally, you can set a custom commit message

          commit_message: "Update snake animation [skip ci]""")


def generate_readme():
    name = input("Enter you name: ")
    bio = input("Enter you bio/short discription: ")
    skills = input("Enter your skills(Comma seperated): ")
    github_username= input("Enter your github username: ")
    linkdin = input("Enter you linkdin URL: ")
    instagram = input("Enter your instagram Username: ")

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
<a href="{linkdin}" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="{linkdin}" height="30" width="40" /></a>

<a href="https://instagram.com/{instagram}" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="{instagram}" height="30" width="40" /></a>

![snake gif](https://github.com/{github_username}/{github_username}/blob/output/github-snake-dark.svg)
        """
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("README.md generated successfully!")

if __name__ == "__main__" :
    generate_readme()





    