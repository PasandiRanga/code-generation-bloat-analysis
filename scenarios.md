# Participant-Facing Scenario Descriptions

Paper: *Beyond Correctness: Empirical Evidence of Output and Prompt Bloat in LLM-Generated Code* (ICTer 2026).

The participant instructions and the four scenario descriptions below are reproduced exactly as they were given to participants. No example function signature, no expected function name, and no instructions on prompt phrasing were included.

## Participant Instructions

Thank you for participating! In this survey, you will read 4 short descriptions of fictional systems and games. Your task is to: (1) Read the scenario. (2) Write a prompt in your own words that you would give to an AI to make it write the exact Python code described. (Please do not just copy-paste the scenario paragraph, write it how you normally talk to an AI!) (3) Test your prompt by pasting it into ChatGPT (GPT-5.5) and Claude (Sonnet 4.6). (4) Share the links to those conversations with us in the form below.

## Scenario 1 - Zorblax Game Scoring

Imagine a fictional game called Zorblax. In this game, players score points by collecting "zaps" and "blitzes." Every zap is worth 7 points, and every blitz is worth 13 points. However, there is a special combo rule: if a player collects strictly more blitzes than zaps in a single round, the points they get from all of their zaps are doubled. Your task is to tell the AI to write a Python function that takes the number of zaps and the number of blitzes as inputs, calculates the final score based on these rules, and returns the total points.

## Scenario 2 - Cargo Manifest Validator

A fictional space delivery company records its cargo shipments using a very specific text format: SHIPID:WEIGHT:DESTINATION. For a record to be considered valid, it must have exactly three parts separated by colons. The SHIPID must be exactly six uppercase letters. The WEIGHT must be a positive whole number. Finally, the DESTINATION must be a single word with no spaces. Your task is to tell the AI to write a Python function that takes a cargo record string as input, checks if it perfectly matches these rules, and returns True if it is valid or False if it is not.

## Scenario 3 - Canteen Credit Decay

Imagine a school cafeteria gives you digital money for food, but to encourage you to spend it quickly, they use a "decay" rule. For the first 7 days, your money is completely safe, but starting on day 8, you lose exactly 10% of whatever money you have left every single day. We need you to write a prompt telling an AI to create a Python function that calculates how much money a student has left. The code must take the starting amount of money and the number of days that have passed as inputs, use this decay rule to calculate the remaining balance, and return the final answer as a decimal number rounded to exactly two places. For this function, assume the student has not spent any of the money; you are only calculating how the original amount shrinks due to time passing.

## Scenario 4 - Pull Request Priority Score

Imagine a fictional code review tool that helps software teams decide which pull requests to review first by calculating a priority score. The rules are simple: add 5 points for every day the pull request has been waiting, and add 2 points for every comment already left on it. However, if the team has marked the pull request as "urgent," the entire score is doubled after adding the points for days and comments together. We need you to write a prompt telling an AI to create a Python function that calculates this priority score. The code must take three inputs, the number of days waiting, the number of comments, and whether it is urgent (True or False), apply this specific scoring logic, and return the final priority score as a whole number.
