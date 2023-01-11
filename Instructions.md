## Work flow Instructions

**Step 01 Fork**
* Create a fork from KNobles/earthquake-prediction
* Copy the main branch only

**Step 02 Clone proyect**
* Clone proyect to your computer
git clone
* ```$ git clone git@github.com:githubUser/earthquake-prediction.git```

```
Cloning into 'earthquake-prediction'...
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 5 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (5/5), done.
```

You will have to repeat this process everytime that you work in a new feature

**Step 03 Create a branch**
* Create a branch, name it as the feature that you will develop. (i.e. prediction)
* Select main branch

**Step 04 Fetch**
* ```$ git fetch --all```
```
Fetching origin
From github.com:DavidValdez89d/earthquake-prediction
 * [new branch]      feature_name -> origin/feature_name
```
**Step 05 go to branch**
* ```$ git checkout feature_name```
```
Branch 'feature_name' set up to track remote branch 'feature_name' from 'origin'.
Switched to a new branch 'feature_name'
```
**Step 06 open the project**
* Open the project in vscode or jupyter-lab
* ```$ code .``` or ```$ jupyter-lab```

**Step 07 check the branch**
* Open a new terminal, and make sure that you are in the correct branch
* ```$ git status```
```
Your branch is up to date with 'origin/feature_name'.
```

**Step 08 work on the code**

**Step 09 Check that everything works**
* your code is not a notebook
* Your work has comments, inputs and outputs are defined
* You have a requeriments.txt file

**Step 10 save the code**
* Save your changes
* Add them to your git ```$ git add .```
* Commit the changes ```$ git commit -m "message"```

**Step 10 push to GitHub**
* push your code ```$ git push```
