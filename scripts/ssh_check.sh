#new
name: SSL Expiry Check

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  check_ssl_expiry:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        with:
          ref: main  # Change this to the default branch of your repository

      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'  # Use Node.js 16

      - name: SSL Expiry Check
        run: |
          ./ssl_check.sh
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          DOMAINS: ${{ secrets.DOMAINS }}
