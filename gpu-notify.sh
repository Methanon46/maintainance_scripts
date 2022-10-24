#!/bin/bash

# WebフックURL（※事前準備で発行したURLを設定する）
WEBHOOK_URL='https://husm.webhook.office.com/webhookb2/62c2a56f-c97c-4fcf-8945-0ac06273c91d@16fbddaa-9f9a-42a5-afbf-d65e420db2fc/IncomingWebhook/f371a2f21034457e8437556e263dde7a/c6f83a96-8b44-4847-985f-33756fd87a73'



# curlコマンド実行
curl -H "Content-Type: application/json" -d "{\"text\": \"メッセージ\"}" $WEBHOOK_URL
