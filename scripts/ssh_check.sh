#!/bin/bash

echo "SLACK_WEBHOOK_URL: $SLACK_WEBHOOK_URL"
echo "DOMAINS_SECRET: $DOMAINS_SECRET"

WEBHOOK_URL="$SLACK_WEBHOOK_URL"

while IFS= read -r DOMAIN; do
    EXPIRY_DATE=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN":443 2>/dev/null | openssl x509 -noout -enddate | cut -d "=" -f 2)
    EXPIRY_TIMESTAMP=$(date -d "$EXPIRY_DATE" +%s)
    CURRENT_TIMESTAMP=$(date +%s)
    DAYS_LEFT=$(( ($EXPIRY_TIMESTAMP - $CURRENT_TIMESTAMP) / 86400 ))

    ALERT_MESSAGE="SSL Expiry Alert\n   * Domain : $DOMAIN\n   * Warning : The SSL certificate for $DOMAIN will expire in $DAYS_LEFT days."

    curl -X POST -H "Content-type: application/json" --data "{\"text\":\"$ALERT_MESSAGE\"}" "$WEBHOOK_URL"
done <<< "$DOMAINS"
