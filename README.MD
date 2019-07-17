# Good Luck

## Concept

以 `linebot` 串連`運勢 api` 傳送每日運勢給訂閱者。  
此範例以 GCP serverless 的方式實作。

![good-luck-structure](https://lh3.googleusercontent.com/9qH_IXVL9Meudjf3rP-oJ3re9h_6vRi8izuum6KKD4xx9-dYe8U7KBn4BlzgHUYQr7TdNlsuf7O9Co1_a6ujla1kkVDIDEDzySuB1d8c7mTRFwH3D7m4qjuej8MX_XTKK4ina55-1VQaUxrJPVbtl3-E95oYcJtf3pAqeJxSdrfT0-5jNs2FbXQQqdaKwVEUUBrt7aI3XG9P1Ya_DqBu7CxrqCbQgUZ0YlkK4q5ZjLXqVhPovDuEPoH4pIKdTM7Tqxb9z3RKWsb_zyImgXypeQNcbZQ1TEMnsoz1hS_zsiNEoWpedLIUzQzRtPzJki7Mi-QAktK2n8MPcREvfdbaSCT8qwKDBOpPVEi4VAl3P0x5qA9MnWcBtAcRFdytP3qmsOzL-lDJqmbdFk39yhJq8D_hz7J7oZZn21U8mx2YBPXqZfidRK_PddsMwLJOWpDNeogwUtsiFjhR9G8wn1k-pLszgSlQIDFWDAhqrKzI5kd-v599o98LJT70FNdS4Sf138cCb8PdIzdGctpuwGW20Y7Z2O1V-r81qEqer779pwYJhfZI4hu2i29ysUjOxmOy3BYYUBnno9jrP3dtEUg9qfYuz9KjSNqUl2GrIOulYr-MfRUpFmPdqiohQiKRJXy7AiffuqBYan8k6Ekcwu3W5UBA4Oa1GGoiLrQGcWxYrM6se38l0UJVITezr8umoJOhQm4R-xKKT3kOnOrTOQ8=w1914-h1216-no)

## 步驟

### 建立 Line@ developer trial 
- [開啟 developer 帳號](https://developers.line.me/en/)
- create provider
- create channel

### 建立一個 GCP 專案

建立一個新的 GCP 專案，之後會在裡面用到
- Cloud Functions
- Cloud Pub/Sub
- Firestore
- Cloud Scheduler

### Firestore

開啟 Firestore 服務，建立一個 collection ，之後給 cloud function 存入使用者的 Line ID 和其它資料使用。

### 建立註冊/取消訂閱的 cloud function

建立一個 cloud function ，觸發條件使用 `http`  

內容帶入  
- reply/main.py 
- reply/requirements.txt 

替換參數
- ACCESS_TOKEN from Line 
- SECRET from Line
- FIRESTORE_PROJECT_ID from Firestore
- COLLECTION_NAME from Firestore

### 建立定期發送運勢的 cloud function

建立一個 cloud function ，觸發條件使用 `Cloud Pub/Sub`，
選取主題`建立新主題`，新增一個 Pub/Sub 主題，給它一個名字 TOPIC_NAME  
內容帶入  
- daily_publish/main.py 
- daily_publish/requirements.txt 

替換參數
- ACCESS_TOKEN from Line 
- SECRET from Line
- FIRESTORE_PROJECT_ID from Firestore
- COLLECTION_NAME from Firestore

### Authenticaton
  
  如果你是自己架 server 串 GCP 的服務，需要建立 [service account](https://cloud.google.com/docs/authentication/production)

  本範例因為全部都是使用 GCP 的服務，google 會自動幫你處理。[Ref.](https://cloud.google.com/docs/authentication/production#providing_credentials_to_your_application)
  >If your application runs on Compute Engine, Kubernetes Engine, the App Engine flexible environment, or Cloud Functions, you don't need to create your own service account. Compute Engine includes a default service account that is automatically created for you, and you can assign a different service account, per-instance, if needed. When you create a new instance, the instance is automatically enabled to run as the default service account and has a default set of authorization permissions. For more information, see Compute Engine default service account. After you set up a service account, ADC can implicitly find your credentials without any need to change your code, as described in the section above. If you want to specifically use Compute Engine credentials, you can explicitly do so, as shown in the following code example.

### Cloud Pub/Sub
確認這裡可以找到剛剛在 Cloud Functions 建立的主題
projects/PROJECT_ID/topics/TOPIC_NAME

### Cloud Scheduler 
建立一個 job ，目標選 Pub/Sub ，主題填 TOPIC_NAME，並設定發佈週期

### 串連 Line Bot

把訂閱/取消 cloud function 的 url 設定在 Line bot 的 Webhook URL  
坑點：
```
Webhook URL cannot be verified
```
驗證不用過也沒關係，但是要確保 https 有通 
    
       
## 使用教學
- 將 Line Bot 加入好友  
- 輸入你的星座來訂閱  
- 輸入 `bye` 來取消訂閱  
- 在 Cloud Scheduler 設定的時間會收到當日星座運勢 

## Reference
[Using Cloud Scheduler and Pub/Sub to Trigger a Cloud Function](https://cloud.google.com/scheduler/docs/tut-pub-sub)  
[Line Messaging API](https://developers.line.biz/en/docs/messaging-api/)  
[horoscope-crawler](https://github.com/andy6804tw/horoscope-crawler)
