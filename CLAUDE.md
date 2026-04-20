# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **pure HTML** presentation for ACM Class 2026 LLM course (CS2916-01). Topic: **Mixture of Experts and Long Context**. Target duration: 40 minutes. Primary language: Chinese, with adequate English for technical content.

The production process (full AI interaction history including prompts) is part of the course submission.

## Conventions

- **Separate styles from content**: keep theme/color/layout config distinct from slide text and images so either can be reworked independently.
- **Image attribution**: whenever an external image is downloaded, record its source URL in a dedicated file alongside it.
- A small demo or hands-on exercise for the audience during the presentation is recommended.

## Git Workflow

- **Never develop on `main`**. If on `main`, ask the user to confirm a branch name before checking out.
- Commit and push after each meaningful change with a descriptive message.
- Do **not** merge branches or open PRs.

## Interaction Guidelines

- Generate only a few slides at a time, then pause for user review before continuing.
- If a required tool or skill is missing, surface it to the user and let them decide whether to install it.
