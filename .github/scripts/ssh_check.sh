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

      - name: Set up environment
        run: |
          chmod +x ssl_check.sh

      - name: SSL Expiry Check
        run: |
          ./ssl_check.sh ${{ secrets.SLACK_WEBHOOK_URL }}
        env:
          DOMAINS: ${{ secrets.DOMAINS }}
