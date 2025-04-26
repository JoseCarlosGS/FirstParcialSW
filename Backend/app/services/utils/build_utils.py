# Archivo build_utils.py para CI/CD
import os
import subprocess
from typing import Dict, Any

def setup_ci_environment(project_dir: str):
    """Configura el entorno para CI/CD"""
    # Crear archivo .gitlab-ci.yml o similar
    ci_content = """
stages:
  - build
  - test
  - deploy

build_angular:
  stage: build
  image: node:16
  script:
    - npm install
    - npm run build
  artifacts:
    paths:
      - dist/

test_angular:
  stage: test
  image: node:16
  script:
    - npm install
    - npm run test

deploy_preview:
  stage: deploy
  image: node:16
  script:
    - npm install -g firebase-tools
    - firebase deploy --token $FIREBASE_TOKEN
  only:
    - master
    """
    
    with open(os.path.join(project_dir, ".gitlab-ci.yml"), "w") as f:
        f.write(ci_content)

def build_project(project_dir: str) -> bool:
    """Compila el proyecto Angular"""
    try:
        subprocess.run(["ng", "build", "--prod"], cwd=project_dir, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run_tests(project_dir: str) -> bool:
    """Ejecuta pruebas del proyecto Angular"""
    try:
        subprocess.run(["ng", "test", "--watch=false"], cwd=project_dir, check=True)
        return True
    except subprocess.CalledProcessError:
        return False