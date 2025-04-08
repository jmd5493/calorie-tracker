# Team Git Branching Guide

This guide will help you stay organized while working on the Calorie Tracker app.

---

## 1. Clone the Repo

```bash
git clone https://github.com/jmd5493/calorie-tracker.git
cd calorie-tracker
```

---

## 2. Checkout Your Feature Branch

Choose your assigned branch:

```bash
git checkout feature/landing-page       # For landing page
git checkout feature/signup-login       # For login/signup
git checkout feature/homepage           # Homepage (James)
git checkout feature/profile-page       # Profile section
```

If you don't see your branch locally, fetch it first:

```bash
git fetch origin
git checkout feature/your-branch-name
```

---

## 3. Make Changes and Push

```bash
git add .
git commit -m "Describe your change"
git push
```

---

## 4. Keep Your Branch Updated with `main`

```bash
git checkout main
git pull origin main

git checkout feature/your-branch-name
git merge main
```

---

## 5. Merge Back into `main` (When Done)

```bash
git checkout main
git pull origin main
git merge feature/your-branch-name
git push origin main
```

---

## ⚔️ 6. If You Get a Merge Conflict

Git will show you what files are conflicting. Open the files and look for:

```
<<<<<<< HEAD
your version
=======
someone else's version
>>>>>>> feature/branch
```

Edit to keep what you want, remove the conflict markers, then:

```bash
git add filename
git commit -m "Resolved merge conflict"
```

---
